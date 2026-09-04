import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.upload_processing import process_uploaded_dataset


DB_PATH = Path("data/processed/sales_analytics.db")
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


def show_upload_panel() -> None:
    st.subheader("Upload New Data")
    st.caption("Upload a pipeline file and any available behavioural history. Files are processed in memory and do not replace the demo dataset.")
    uploads = {}
    for filename in UPLOAD_NAMES:
        label = filename if filename == "sales_pipeline.csv" else f"{filename} (optional)"
        uploaded = st.file_uploader(label, type="csv", key=f"upload_{filename}")
        if uploaded is not None:
            uploads[filename] = uploaded

    if uploads:
        st.write("Uploaded file preview")
        preview_tabs = st.tabs(list(uploads))
        for tab, (filename, uploaded) in zip(preview_tabs, uploads.items()):
            with tab:
                try:
                    uploaded.seek(0)
                    preview = pd.read_csv(uploaded)
                    st.caption(f"{len(preview):,} rows | {len(preview.columns):,} columns")
                    st.dataframe(preview.head(5), width="stretch")
                except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError) as error:
                    st.error(f"{filename}: could not preview this CSV ({error}).")

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


def apply_filters(data: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filters")
    agents = st.sidebar.multiselect("Sales Agent", sorted(data["sales_agent"].dropna().unique()))
    stages = st.sidebar.multiselect("Deal Stage", sorted(data["deal_stage"].dropna().unique()))
    products = st.sidebar.multiselect("Product", sorted(data["product"].dropna().unique()))
    accounts = st.sidebar.multiselect("Account", sorted(data["account"].fillna("Unknown").unique()))

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
        date_range = st.sidebar.date_input("Engaged Between", value=(min_date, max_date), min_value=min_date, max_value=max_date)
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
            engaged = pd.to_datetime(filtered["engage_date"], errors="coerce")
            filtered = filtered[engaged.dt.date.between(start_date, end_date)]

    return filtered


def show_opportunity_explorer(data: pd.DataFrame) -> None:
    st.subheader("Opportunity Explorer")
    choices = data["opportunity_id"].astype(str).tolist()
    selected = st.selectbox("Select an opportunity", ["Select an opportunity"] + choices)
    if selected == "Select an opportunity":
        st.caption("Select an opportunity to inspect its sales and behavioural profile.")
        return

    opportunity = data[data["opportunity_id"].astype(str).eq(selected)].iloc[0]
    available = [column for column in DETAIL_COLUMNS if column in opportunity.index]
    detail = opportunity[available].to_frame("Value")
    detail.index = [column.replace("_", " ").title() for column in detail.index]
    detail.loc["Behavioural History Available"] = "Yes" if opportunity["has_behavioural_history"] else "No history available"
    st.dataframe(detail, width="stretch")


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
    st.subheader("Sales Pipeline")
    stage_counts = filtered["deal_stage"].value_counts().rename_axis("deal_stage").reset_index(name="opportunities")
    if stage_counts.empty:
        st.info("No opportunities match the current filters.")
    else:
        st.plotly_chart(px.bar(stage_counts, x="deal_stage", y="opportunities", title="Opportunities by Deal Stage"), width="stretch")

    st.subheader("Trends Over Time")
    engaged = filtered.copy()
    engaged["engage_month"] = pd.to_datetime(engaged["engage_date"], errors="coerce").dt.to_period("M").dt.to_timestamp()
    monthly_engagements = engaged.dropna(subset=["engage_month"]).groupby("engage_month").size().reset_index(name="opportunities")

    closed_dated = closed.copy()
    closed_dated["close_month"] = pd.to_datetime(closed_dated["close_date"], errors="coerce").dt.to_period("M").dt.to_timestamp()
    monthly_outcomes = closed_dated.dropna(subset=["close_month"]).groupby("close_month").agg(
        closed=("opportunity_id", "count"), won=("is_won", "sum"),
    ).reset_index()
    monthly_outcomes["win_rate"] = monthly_outcomes["won"] / monthly_outcomes["closed"] * 100

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
            trend_columns[1].plotly_chart(
                px.line(monthly_outcomes, x="close_month", y="win_rate", markers=True, title="Win Rate by Month (Closed Deals)"),
                width="stretch",
            )

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

    st.subheader("Won vs Lost Behaviour")
    outcome_summary = closed.groupby("deal_stage").agg(
        opportunities=("opportunity_id", "count"), response_rate=("response_rate", "mean"),
        response_time=("avg_response_time_hours", "mean"), activities=("activity_count", "mean"),
        stage_transitions=("stage_transition_count", "mean"),
    ).reset_index()
    if not outcome_summary.empty:
        st.dataframe(outcome_summary, width="stretch")

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

    st.subheader("Sales Agent Performance")
    agent_summary = filtered.groupby("sales_agent").agg(
        opportunities=("opportunity_id", "count"), avg_deal_duration=("deal_duration_days", "mean"),
        avg_response_rate=("response_rate", "mean"), avg_activity_count=("activity_count", "mean"),
    ).reset_index().sort_values("avg_deal_duration")
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

    st.subheader("Deal Duration by Product")
    product_summary = closed.groupby("product").agg(avg_duration=("deal_duration_days", "mean"), deals=("opportunity_id", "count")).reset_index()
    if not product_summary.empty:
        st.plotly_chart(px.bar(product_summary, x="product", y="avg_duration", title="Average Deal Duration by Product"), width="stretch")
        st.download_button(
            "Download product summary (CSV)", data=to_csv_bytes(product_summary),
            file_name="product_summary.csv", mime="text/csv", key="download_product_summary",
        )

    show_opportunity_explorer(filtered)

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
