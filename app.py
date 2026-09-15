import io
import sqlite3
import zipfile
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.email_report import DEFAULT_THRESHOLDS, build_report_html, evaluate_alerts, send_email_report
from src.upload_processing import process_uploaded_dataset


DB_PATH = Path("data/processed/sales_analytics.db")
KPI_SQL_PATH = Path("sql/kpis.sql")
UPLOAD_NAMES = [
    "sales_pipeline.csv",
    "email_history.csv",
    "crm_activities.csv",
    "stage_history.csv",
]
DETAIL_COLUMNS = [
    "opportunity_id", "sales_agent", "account", "product", "deal_stage",
    "close_value", "engage_date", "close_date", "deal_duration_days", "deal_speed",
    "is_closed", "is_won", "email_count", "responded_email_count", "response_rate",
    "avg_response_time_hours", "median_response_time_hours", "activity_count",
    "successful_activity_count", "call_count", "meeting_count", "demo_count",
    "followup_count", "unique_activity_types", "stage_transition_count",
    "total_stage_days", "avg_stage_days", "has_behavioural_history", "engagement_level",
]


st.set_page_config(page_title="Sales Behaviour Analytics", layout="wide")


@st.cache_data
def to_csv_bytes(data: pd.DataFrame) -> bytes:
    return data.to_csv(index=False).encode("utf-8")


@st.cache_data
def load_demo_data() -> pd.DataFrame:
    if not DB_PATH.exists():
        return pd.DataFrame()
    with sqlite3.connect(DB_PATH) as connection:
        return pd.read_sql("SELECT * FROM opportunity_features", connection)


@st.cache_data
def load_kpi_queries() -> dict[str, str]:
    """Parse sql/kpis.sql into {comment title: query text} for on-dashboard transparency."""
    if not KPI_SQL_PATH.exists():
        return {}
    queries: dict[str, str] = {}
    title, lines = None, []
    for line in KPI_SQL_PATH.read_text().splitlines():
        if line.startswith("-- "):
            if title and lines:
                queries[title] = "\n".join(lines).strip()
            title, lines = line[3:].strip(), []
        elif title is not None:
            lines.append(line)
    if title and lines:
        queries[title] = "\n".join(lines).strip()
    return queries


def show_sql(title: str) -> None:
    query = load_kpi_queries().get(title)
    if query:
        with st.expander("How is this calculated? (SQL)"):
            st.code(query, language="sql")


def show_upload_panel() -> None:
    st.subheader("Upload New Data")
    st.caption("Upload a pipeline file (CSV or JSON) and any available behavioural history (CSV). Files are processed in memory and do not replace the demo dataset.")
    uploads = {}
    for filename in UPLOAD_NAMES:
        is_pipeline = filename == "sales_pipeline.csv"
        label = filename if is_pipeline else f"{filename} (optional)"
        uploaded = st.file_uploader(label, type=["csv", "json"] if is_pipeline else "csv", key=f"upload_{filename}")
        if uploaded is not None:
            uploads[filename] = uploaded

    if uploads:
        st.write("Uploaded file preview")
        preview_tabs = st.tabs(list(uploads))
        for tab, (filename, uploaded) in zip(preview_tabs, uploads.items()):
            with tab:
                try:
                    uploaded.seek(0)
                    preview = pd.read_json(uploaded) if uploaded.name.endswith(".json") else pd.read_csv(uploaded)
                    st.caption(f"{len(preview):,} rows | {len(preview.columns):,} columns")
                    st.dataframe(preview.head(5), width="stretch")
                except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError, ValueError) as error:
                    st.error(f"{filename}: could not preview this file ({error}).")

    if st.button("Validate and process uploads", type="primary", disabled="sales_pipeline.csv" not in uploads):
        try:
            features, _ = process_uploaded_dataset(uploads)
        except ValueError as error:
            st.session_state.pop("uploaded_features", None)
            st.error(f"Upload failed:\n\n{error}")
        else:
            st.session_state["uploaded_features"] = features
            st.success(f"Upload processed successfully: {len(features):,} opportunities and {len(features.columns):,} analytical columns.")

    if "uploaded_features" in st.session_state:
        st.info("Uploaded dataset is ready. Select it from the Dataset selector to view its analytics.")


FILTER_STATE_KEYS = ["filter_agents", "filter_stages", "filter_products", "filter_accounts", "filter_date_range"]


def apply_filters(data: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filters")
    if st.sidebar.button("Reset Filters", key="reset_filters_button"):
        for key in FILTER_STATE_KEYS:
            st.session_state.pop(key, None)
        st.rerun()

    agents = st.sidebar.multiselect("Sales Agent", sorted(data["sales_agent"].dropna().unique()), key="filter_agents")
    stages = st.sidebar.multiselect("Deal Stage", sorted(data["deal_stage"].dropna().unique()), key="filter_stages")
    products = st.sidebar.multiselect("Product", sorted(data["product"].dropna().unique()), key="filter_products")
    accounts = st.sidebar.multiselect("Account", sorted(data["account"].fillna("Unknown").unique()), key="filter_accounts")

    filtered = data.copy()
    if agents:
        filtered = filtered[filtered["sales_agent"].isin(agents)]
    if stages:
        filtered = filtered[filtered["deal_stage"].isin(stages)]
    if products:
        filtered = filtered[filtered["product"].isin(products)]
    if accounts:
        filtered = filtered[filtered["account"].fillna("Unknown").isin(accounts)]

    engage_dates = pd.to_datetime(data["engage_date"], errors="coerce").dropna()
    if not engage_dates.empty:
        min_date, max_date = engage_dates.min().date(), engage_dates.max().date()
        date_range = st.sidebar.date_input(
            "Engaged Between", value=(min_date, max_date), min_value=min_date, max_value=max_date, key="filter_date_range",
        )
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
            engaged = pd.to_datetime(filtered["engage_date"], errors="coerce")
            filtered = filtered[engaged.dt.date.between(start_date, end_date)]

    return filtered


def _opportunity_detail(data: pd.DataFrame, opportunity_id: str) -> pd.DataFrame:
    opportunity = data[data["opportunity_id"].astype(str).eq(opportunity_id)].iloc[0]
    available = [column for column in DETAIL_COLUMNS if column in opportunity.index]
    detail = opportunity[available].to_frame("Value")
    detail.index = [column.replace("_", " ").title() for column in detail.index]
    detail.loc["Behavioural History Available"] = "Yes" if opportunity["has_behavioural_history"] else "No history available"
    return detail


def show_opportunity_explorer(data: pd.DataFrame) -> None:
    st.subheader("Opportunity Explorer")
    choices = data["opportunity_id"].astype(str).tolist()
    no_selection = "Select an opportunity"

    compare = st.checkbox("Compare two opportunities side by side")
    if not compare:
        selected = st.selectbox("Select an opportunity", [no_selection] + choices)
        if selected == no_selection:
            st.caption("Select an opportunity to inspect its sales and behavioural profile.")
            return
        st.dataframe(_opportunity_detail(data, selected), width="stretch")
        return

    left_column, right_column = st.columns(2)
    with left_column:
        first = st.selectbox("First opportunity", [no_selection] + choices, key="compare_first")
    with right_column:
        second = st.selectbox("Second opportunity", [no_selection] + choices, key="compare_second")

    if first == no_selection or second == no_selection:
        st.caption("Select two opportunities to compare their sales and behavioural profiles.")
        return

    comparison = _opportunity_detail(data, first).rename(columns={"Value": first})
    comparison[second] = _opportunity_detail(data, second)["Value"]
    st.dataframe(comparison, width="stretch")


def show_alerts_and_reporting(data: pd.DataFrame, dataset_label: str) -> None:
    st.subheader("Alert Monitoring")
    st.caption("Descriptive threshold checks against the current selection - not predictions.")
    with st.expander("Configure thresholds"):
        threshold_columns = st.columns(3)
        min_win_rate = threshold_columns[0].number_input(
            "Minimum win rate (%)", 0.0, 100.0, DEFAULT_THRESHOLDS["min_win_rate"], key="threshold_win_rate",
        )
        min_response_rate = threshold_columns[1].number_input(
            "Minimum response rate (%)", 0.0, 100.0, DEFAULT_THRESHOLDS["min_response_rate"], key="threshold_response_rate",
        )
        max_response_time = threshold_columns[2].number_input(
            "Maximum avg response time (hours)", 0.0, 200.0, DEFAULT_THRESHOLDS["max_avg_response_time_hours"], key="threshold_response_time",
        )
    thresholds = {
        "min_win_rate": min_win_rate,
        "min_response_rate": min_response_rate,
        "max_avg_response_time_hours": max_response_time,
    }
    alerts = evaluate_alerts(data, thresholds)
    if not alerts:
        st.success("No thresholds breached for the current selection.")
    else:
        for alert in alerts:
            show = st.error if alert["severity"] == "high" else st.warning
            show(f"[{alert['severity'].upper()}] {alert['message']}")

    st.subheader("Share This Report")
    closed = data[data["is_closed"] == 1]
    won = data[data["is_won"] == 1]
    win_rate = len(won) / len(closed) * 100 if len(closed) else 0
    metrics = {
        "Opportunities": f"{len(data):,}",
        "Closed Deals": f"{len(closed):,}",
        "Win Rate": f"{win_rate:.1f}%",
        "Average Response Rate": f"{data['response_rate'].mean() * 100:.1f}%" if data["response_rate"].notna().any() else "N/A",
        "Average Response Time": f"{data['avg_response_time_hours'].mean():.1f}h" if data["avg_response_time_hours"].notna().any() else "N/A",
    }
    recipient = st.text_input("Recipient email", key="report_recipient")
    if st.button("Email this report"):
        if not recipient:
            st.error("Enter a recipient email address first.")
        else:
            html = build_report_html(dataset_label, metrics, alerts)
            success, message = send_email_report(recipient, f"Sales Behaviour Analytics - {dataset_label}", html)
            (st.success if success else st.error)(message)


def _compute_agent_summary(filtered: pd.DataFrame) -> pd.DataFrame:
    return filtered.groupby("sales_agent").agg(
        opportunities=("opportunity_id", "count"), avg_deal_duration=("deal_duration_days", "mean"),
        avg_response_rate=("response_rate", "mean"), avg_activity_count=("activity_count", "mean"),
    ).reset_index().sort_values("avg_deal_duration")


def _compute_product_summary(closed: pd.DataFrame) -> pd.DataFrame:
    return closed.groupby("product").agg(
        avg_duration=("deal_duration_days", "mean"), deals=("opportunity_id", "count"),
    ).reset_index()


def build_report_bundle(
    filtered: pd.DataFrame, agent_summary: pd.DataFrame, product_summary: pd.DataFrame,
    dataset_label: str, metrics: dict[str, str], alerts: list[dict[str, str]],
) -> tuple[bytes, str]:
    """Zip the filtered data, summary tables, and an HTML report into one traceable-filename download."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    safe_label = dataset_label.lower().replace(" ", "_")
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("filtered_opportunities.csv", filtered.to_csv(index=False))
        archive.writestr("agent_summary.csv", agent_summary.to_csv(index=False))
        archive.writestr("product_summary.csv", product_summary.to_csv(index=False))
        archive.writestr("summary_report.html", build_report_html(dataset_label, metrics, alerts))
    return buffer.getvalue(), f"dealmakers_report_{safe_label}_{timestamp}.zip"


def show_overview(filtered: pd.DataFrame, closed: pd.DataFrame, won: pd.DataFrame, dataset_label: str) -> None:
    win_rate = len(won) / len(closed) * 100 if len(closed) else 0
    median_duration = closed["deal_duration_days"].median() if len(closed) else 0

    columns = st.columns(6)
    columns[0].metric("Opportunities", f"{len(filtered):,}")
    columns[1].metric("Closed Deals", f"{len(closed):,}")
    columns[2].metric("Won Deals", f"{len(won):,}")
    columns[3].metric("Win Rate", f"{win_rate:.1f}%")
    columns[4].metric("Median Deal Duration", f"{median_duration:.0f} days")
    columns[5].metric("Won Revenue", f"${won['close_value'].sum():,.0f}")

    st.download_button(
        "Download filtered opportunities (CSV)",
        data=to_csv_bytes(filtered),
        file_name="filtered_opportunities.csv",
        mime="text/csv",
    )

    st.divider()
    st.subheader("Export Full Report Bundle")
    st.caption("Filtered data, agent and product summaries, and an HTML KPI report, zipped with a timestamped filename.")
    agent_summary = _compute_agent_summary(filtered)
    product_summary = _compute_product_summary(closed)
    metrics = {
        "Opportunities": f"{len(filtered):,}",
        "Closed Deals": f"{len(closed):,}",
        "Win Rate": f"{win_rate:.1f}%",
        "Average Response Rate": f"{filtered['response_rate'].mean() * 100:.1f}%" if filtered["response_rate"].notna().any() else "N/A",
        "Average Response Time": f"{filtered['avg_response_time_hours'].mean():.1f}h" if filtered["avg_response_time_hours"].notna().any() else "N/A",
    }
    alerts = evaluate_alerts(filtered, DEFAULT_THRESHOLDS)
    bundle_bytes, bundle_name = build_report_bundle(filtered, agent_summary, product_summary, dataset_label, metrics, alerts)
    st.download_button("Download Full Report Bundle (ZIP)", data=bundle_bytes, file_name=bundle_name, mime="application/zip")


def show_pipeline_funnel_and_trends(filtered: pd.DataFrame, closed: pd.DataFrame) -> None:
    st.subheader("Sales Pipeline")
    stage_counts = filtered["deal_stage"].value_counts().rename_axis("deal_stage").reset_index(name="opportunities")
    if stage_counts.empty:
        st.info("No opportunities match the current filters.")
    else:
        st.plotly_chart(px.bar(stage_counts, x="deal_stage", y="opportunities", title="Opportunities by Deal Stage"), width="stretch")
    show_sql("Pipeline funnel")

    st.subheader("Pipeline Funnel and Drop-Off")
    st.caption("Cumulative counts of opportunities that reached each stage, based on the documented flow Prospecting -> Engaging -> Won/Lost. Not currently-in-stage snapshots, which would understate progression since Won/Lost opportunities have already left Prospecting and Engaging.")
    stage_totals = filtered["deal_stage"].value_counts()
    reached_engaging_or_beyond = int(stage_totals.reindex(["Engaging", "Won", "Lost"], fill_value=0).sum())
    funnel_data = pd.DataFrame({
        "stage": ["Reached Prospecting", "Reached Engaging", "Won"],
        "opportunities": [len(filtered), reached_engaging_or_beyond, int(stage_totals.get("Won", 0))],
    })
    if funnel_data["opportunities"].iloc[0] == 0:
        st.info("No opportunities match the current filters.")
    else:
        funnel_data["drop_off_pct"] = funnel_data["opportunities"].pct_change().mul(-100)
        st.plotly_chart(px.funnel(funnel_data, x="opportunities", y="stage", title="Pipeline Funnel (Prospecting to Won)"), width="stretch")
        display = funnel_data.rename(columns={"stage": "Stage", "opportunities": "Opportunities"})
        display["drop_off_pct"] = display["drop_off_pct"].map(lambda value: f"{value:.1f}%" if pd.notna(value) else "-")
        display = display.rename(columns={"drop_off_pct": "Drop-off vs Previous Stage"})
        st.dataframe(display, width="stretch")
        st.caption(f"Lost: {int(stage_totals.get('Lost', 0)):,} opportunities (counted as having reached Engaging, per the documented flow).")

    st.subheader("Trends Over Time")
    engaged = filtered.copy()
    engaged["engage_month"] = pd.to_datetime(engaged["engage_date"], errors="coerce").dt.to_period("M").dt.to_timestamp()
    monthly_engagements = engaged.dropna(subset=["engage_month"]).groupby("engage_month").size().reset_index(name="opportunities")
    if not monthly_engagements.empty:
        monthly_engagements = monthly_engagements.sort_values("engage_month")
        monthly_engagements["cumulative_opportunities"] = monthly_engagements["opportunities"].cumsum()

    closed_dated = closed.copy()
    closed_dated["close_month"] = pd.to_datetime(closed_dated["close_date"], errors="coerce").dt.to_period("M").dt.to_timestamp()
    monthly_outcomes = closed_dated.dropna(subset=["close_month"]).groupby("close_month").agg(
        closed=("opportunity_id", "count"), won=("is_won", "sum"),
    ).reset_index()
    if not monthly_outcomes.empty:
        monthly_outcomes = monthly_outcomes.sort_values("close_month")
        monthly_outcomes["win_rate"] = monthly_outcomes["won"] / monthly_outcomes["closed"] * 100
        monthly_outcomes["win_rate_rolling_3mo"] = monthly_outcomes["win_rate"].rolling(3, min_periods=1).mean()

    if monthly_engagements.empty and monthly_outcomes.empty:
        st.info("No dated opportunities available for a trend view with the current filters.")
    else:
        trend_columns = st.columns(2)
        if not monthly_engagements.empty:
            trend_columns[0].plotly_chart(
                px.line(monthly_engagements, x="engage_month", y="opportunities", markers=True, title="Opportunities Engaged by Month"),
                width="stretch",
            )
        if not monthly_outcomes.empty:
            win_rate_long = monthly_outcomes.melt(
                id_vars="close_month", value_vars=["win_rate", "win_rate_rolling_3mo"], var_name="series", value_name="value",
            )
            win_rate_long["series"] = win_rate_long["series"].map({"win_rate": "Monthly", "win_rate_rolling_3mo": "3-Month Rolling Average"})
            trend_columns[1].plotly_chart(
                px.line(win_rate_long, x="close_month", y="value", color="series", markers=True, title="Win Rate by Month (with Rolling Average)"),
                width="stretch",
            )
        if not monthly_engagements.empty:
            st.plotly_chart(
                px.area(monthly_engagements, x="engage_month", y="cumulative_opportunities", title="Cumulative Opportunities Engaged"),
                width="stretch",
            )
    show_sql("Month-over-month win rate change for closed deals (CTE + window function: LAG)")


def show_distribution_and_correlation(filtered: pd.DataFrame, closed: pd.DataFrame, won: pd.DataFrame) -> None:
    st.subheader("Distribution Analysis")
    distribution_columns = st.columns(2)
    if closed["deal_duration_days"].notna().any():
        duration_skew = closed["deal_duration_days"].skew()
        distribution_columns[0].plotly_chart(
            px.histogram(closed, x="deal_duration_days", title="Deal Duration Distribution (Closed Deals)"), width="stretch",
        )
        distribution_columns[0].caption(f"Skewness: {duration_skew:.2f} ({'right-skewed' if duration_skew > 0.5 else 'left-skewed' if duration_skew < -0.5 else 'roughly symmetric'})")
    if won["close_value"].notna().any():
        value_skew = won["close_value"].skew()
        distribution_columns[1].plotly_chart(
            px.histogram(won, x="close_value", title="Close Value Distribution (Won Deals)"), width="stretch",
        )
        distribution_columns[1].caption(f"Skewness: {value_skew:.2f} ({'right-skewed' if value_skew > 0.5 else 'left-skewed' if value_skew < -0.5 else 'roughly symmetric'}). {int(won['is_close_value_outlier'].sum())} statistical outliers (IQR method).")

    st.subheader("Correlation Analysis")
    correlation_columns = ["response_rate", "avg_response_time_hours", "activity_count", "deal_duration_days", "close_value", "stage_transition_count"]
    available_columns = [column for column in correlation_columns if column in filtered.columns and filtered[column].notna().any()]
    correlation_method = st.radio("Correlation method", ["pearson", "spearman"], horizontal=True, key="correlation_method")
    if len(available_columns) >= 2:
        correlation_matrix = filtered[available_columns].corr(method=correlation_method)
        st.plotly_chart(
            px.imshow(correlation_matrix, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1, title=f"{correlation_method.title()} Correlation Between Numeric Features"),
            width="stretch",
        )
    else:
        st.info("Not enough numeric fields with data in the current selection to compute correlations.")


def show_behavioural_analysis(filtered: pd.DataFrame, closed: pd.DataFrame) -> None:
    st.subheader("Behavioural Patterns by Deal Speed")
    speed_summary = closed.groupby("deal_speed").agg(
        response_rate=("response_rate", "mean"),
        avg_response_time=("avg_response_time_hours", "mean"),
        activity_count=("activity_count", "mean"),
        followup_count=("followup_count", "mean"),
        deals=("opportunity_id", "count"),
    ).reset_index()
    if speed_summary.empty:
        st.info("Closed-deal behavioural comparisons are unavailable for this selection.")
    else:
        display = speed_summary.rename(columns={
            "deal_speed": "Deal speed", "response_rate": "Average response rate",
            "avg_response_time": "Average response time (hours)",
            "activity_count": "Average CRM activities per opportunity",
            "followup_count": "Average follow-ups per opportunity", "deals": "Closed opportunities",
        })
        st.dataframe(display.style.format({
            "Average response rate": "{:.1%}", "Average response time (hours)": "{:.1f}",
            "Average CRM activities per opportunity": "{:.1f}", "Average follow-ups per opportunity": "{:.1f}",
        }), width="stretch")
        st.plotly_chart(px.scatter(
            closed, x="avg_response_time_hours", y="deal_duration_days", color="deal_speed",
            hover_data=["opportunity_id", "sales_agent", "deal_stage"], title="Response Time vs Deal Duration",
        ), width="stretch")
    show_sql("Behaviour by deal speed")

    st.subheader("Won vs Lost Behaviour")
    outcome_summary = closed.groupby("deal_stage").agg(
        opportunities=("opportunity_id", "count"), response_rate=("response_rate", "mean"),
        response_time=("avg_response_time_hours", "mean"), activities=("activity_count", "mean"),
        stage_transitions=("stage_transition_count", "mean"),
    ).reset_index()
    if not outcome_summary.empty:
        st.dataframe(outcome_summary, width="stretch")
    show_sql("Won versus Lost behavioural comparison (closed opportunities only)")

    st.subheader("Engagement-Level Comparison")
    engagement_summary = filtered.groupby("engagement_level").agg(
        opportunities=("opportunity_id", "count"),
        closed_deals=("is_closed", "sum"),
        win_rate=("is_won", "mean"),
        response_rate=("response_rate", "mean"),
        activities=("activity_count", "mean"),
    ).reset_index()
    if not engagement_summary.empty:
        st.dataframe(engagement_summary, width="stretch")
    show_sql("Win rate by descriptive engagement level")

    st.subheader("Coaching Signals")
    fast = speed_summary[speed_summary["deal_speed"] == "Fast"]
    slow = speed_summary[speed_summary["deal_speed"] == "Slow"]
    if not fast.empty and not slow.empty:
        st.write(f"- Fast deals show a {(fast['response_rate'].iloc[0] - slow['response_rate'].iloc[0]):.1%} difference in average response rate compared with slow deals.")
        st.write(f"- The observed average response-time difference is {abs(fast['avg_response_time'].iloc[0] - slow['avg_response_time'].iloc[0]):.1f} hours.")
        st.write(f"- Fast deals average {(fast['activity_count'].iloc[0] - slow['activity_count'].iloc[0]):.1f} more CRM activities than slow deals.")
    else:
        st.info("Coaching comparisons need both Fast and Slow closed-deal groups.")
    st.warning("Behavioural history may be simulated for analytical prototyping. Treat these signals as associations, not causal conclusions.")


def show_agents_and_products(filtered: pd.DataFrame, closed: pd.DataFrame) -> None:
    st.subheader("Sales Agent Performance")
    agent_summary = _compute_agent_summary(filtered)
    st.dataframe(agent_summary.head(15).style.format({
        "avg_deal_duration": "{:.1f}", "avg_response_rate": "{:.1%}", "avg_activity_count": "{:.1f}",
    }), width="stretch")
    if not agent_summary.empty:
        st.download_button(
            "Download agent summary (CSV)", data=to_csv_bytes(agent_summary),
            file_name="agent_summary.csv", mime="text/csv", key="download_agent_summary",
        )
        selected_agent = st.selectbox("Inspect a sales agent", agent_summary["sales_agent"].tolist())
        agent = filtered[filtered["sales_agent"] == selected_agent]
        agent_closed = agent[agent["is_closed"] == 1]
        agent_won = agent[agent["is_won"] == 1]
        agent_columns = st.columns(4)
        agent_columns[0].metric("Agent Opportunities", f"{len(agent):,}")
        agent_columns[1].metric("Agent Win Rate", f"{len(agent_won) / len(agent_closed) * 100:.1f}%" if len(agent_closed) else "0.0%")
        agent_columns[2].metric("Agent Response Rate", f"{agent['response_rate'].mean():.1%}")
        agent_columns[3].metric("Agent Activities", f"{agent['activity_count'].mean():.1f}")
    show_sql("Sales-agent behavioural and outcome comparison")

    st.subheader("Deal Duration by Product")
    product_summary = _compute_product_summary(closed)
    if not product_summary.empty:
        st.plotly_chart(px.bar(product_summary, x="product", y="avg_duration", title="Average Deal Duration by Product"), width="stretch")
        st.download_button(
            "Download product summary (CSV)", data=to_csv_bytes(product_summary),
            file_name="product_summary.csv", mime="text/csv", key="download_product_summary",
        )
    show_sql("Product outcome and behavioural comparison")


DASHBOARD_PAGES = [
    "Overview",
    "Pipeline, Funnel & Trends",
    "Distribution & Correlation",
    "Behavioural Analysis",
    "Agents & Products",
    "Opportunity Explorer",
    "Alerts & Reporting",
]


def show_dashboard(data: pd.DataFrame, dataset_label: str) -> None:
    st.title("Sales Behaviour Analytics")
    st.caption(f"{dataset_label} | Behavioural patterns associated with deal progression and closure")
    with st.expander("How to read this dashboard", expanded=True):
        st.markdown(
            "- **Response rate** is the percentage of emails that received a customer response.\n"
            "- **Response time** is the average number of hours a customer took to reply.\n"
            "- **Deal duration** is measured from engagement to close for closed opportunities.\n"
            "- Behavioural history may be simulated; all findings are descriptive associations, not causal conclusions."
        )

    filtered = apply_filters(data)
    closed = filtered[filtered["is_closed"] == 1]
    won = filtered[filtered["is_won"] == 1]

    st.sidebar.header("Dashboard Section")
    page = st.sidebar.radio("Go to", DASHBOARD_PAGES, key="dashboard_page", label_visibility="collapsed")
    st.divider()

    if page == "Overview":
        show_overview(filtered, closed, won, dataset_label)
    elif page == "Pipeline, Funnel & Trends":
        show_pipeline_funnel_and_trends(filtered, closed)
    elif page == "Distribution & Correlation":
        show_distribution_and_correlation(filtered, closed, won)
    elif page == "Behavioural Analysis":
        show_behavioural_analysis(filtered, closed)
    elif page == "Agents & Products":
        show_agents_and_products(filtered, closed)
    elif page == "Opportunity Explorer":
        show_opportunity_explorer(filtered)
    elif page == "Alerts & Reporting":
        show_alerts_and_reporting(filtered, dataset_label)


demo_data = load_demo_data()
if demo_data.empty:
    st.error("Analytics database not found. Run `.venv/bin/python src/load_database.py` first.")
    st.stop()

st.sidebar.header("Dataset")
dataset_mode = st.sidebar.radio("View", ["Demo Dataset", "Uploaded Dataset"])
if dataset_mode == "Uploaded Dataset":
    show_upload_panel()
    if "uploaded_features" not in st.session_state:
        st.info("Upload and process a sales_pipeline.csv file to view uploaded analytics.")
        st.stop()
    current_data = st.session_state["uploaded_features"]
    show_dashboard(current_data, "Uploaded Dataset")
else:
    show_dashboard(demo_data, "Demo Dataset")
