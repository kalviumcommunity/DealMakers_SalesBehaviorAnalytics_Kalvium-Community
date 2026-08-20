import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px


DB_PATH = Path("data/processed/sales_analytics.db")


st.set_page_config(
    page_title="Sales Behaviour Analytics",
    layout="wide"
)

if not DB_PATH.exists():
    st.error("Analytics database not found. Run `.venv/bin/python src/load_database.py` first.")
    st.stop()


@st.cache_data
def load_data():
    connection = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM opportunity_features",
        connection
    )

    connection.close()

    return df


df = load_data()

st.title("Sales Behaviour Analytics")
st.caption(
    "Behavioural patterns associated with deal progression "
    "and closure"
)

with st.expander("How to read this dashboard", expanded=True):
    st.markdown(
        "- **Opportunity**: one potential sales deal in the CRM.\n"
        "- **Response rate**: percentage of emails that received a customer response.\n"
        "- **Response time**: average number of **hours** a customer took to reply; lower means a faster reply.\n"
        "- **Activity count**: average number of logged CRM activities per opportunity, including calls, meetings, demos, follow-ups, and sales emails.\n"
        "- **Deal duration**: days between engagement and close for a closed opportunity.\n"
        "- These are simulated behavioural signals and show associations, not proof that one behaviour caused an outcome."
    )

st.sidebar.header("Filters")

agents = st.sidebar.multiselect(
    "Sales Agent",
    sorted(df["sales_agent"].dropna().unique())
)

stages = st.sidebar.multiselect(
    "Deal Stage",
    sorted(df["deal_stage"].dropna().unique())
)

products = st.sidebar.multiselect(
    "Product",
    sorted(df["product"].dropna().unique())
)

accounts = st.sidebar.multiselect(
    "Account",
    sorted(df["account"].fillna("Unknown").unique())
)


filtered = df.copy()

if agents:
    filtered = filtered[
        filtered["sales_agent"].isin(agents)
    ]

if stages:
    filtered = filtered[
        filtered["deal_stage"].isin(stages)
    ]

if products:
    filtered = filtered[
        filtered["product"].isin(products)
    ]

if accounts:
    filtered = filtered[
        filtered["account"].fillna("Unknown").isin(accounts)
    ]


# -----------------------------
# KPIs
# -----------------------------

total_opportunities = len(filtered)

closed = filtered[
    filtered["is_closed"] == 1
]

won = filtered[
    filtered["is_won"] == 1
]

win_rate = (
    len(won) / len(closed) * 100
    if len(closed) > 0
    else 0
)

median_duration = (
    closed["deal_duration_days"].median()
    if len(closed) > 0
    else 0
)

avg_deal_value = (
    closed["close_value"].mean()
    if len(closed) > 0
    else 0
)

total_revenue = won["close_value"].sum()


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Opportunities",
    f"{total_opportunities:,}"
)

col2.metric(
    "Win Rate",
    f"{win_rate:.1f}%"
)

col3.metric(
    "Median Deal Duration",
    f"{median_duration:.0f} days"
)

col4.metric(
    "Average Deal Value",
    f"${avg_deal_value:,.0f}"
)

col5.metric(
    "Won Revenue",
    f"${total_revenue:,.0f}"
)


st.divider()


# -----------------------------
# Deal funnel
# -----------------------------

st.subheader("Sales Pipeline")

stage_counts = (
    filtered["deal_stage"]
    .value_counts()
    .reset_index()
)

stage_counts.columns = [
    "deal_stage",
    "opportunities"
]

fig_funnel = px.bar(
    stage_counts,
    x="deal_stage",
    y="opportunities",
    title="Opportunities by Deal Stage"
)

st.plotly_chart(
    fig_funnel,
    use_container_width=True
)


# -----------------------------
# Behaviour vs deal speed
# -----------------------------

st.subheader(
    "Behavioural Patterns by Deal Speed"
)

closed_speed = filtered[
    filtered["is_closed"] == 1
]

speed_summary = (
    closed_speed.groupby("deal_speed")
    .agg(
        response_rate=("response_rate", "mean"),
        avg_response_time=(
            "avg_response_time_hours",
            "mean"
        ),
        activity_count=(
            "activity_count",
            "mean"
        ),
        followup_count=(
            "followup_count",
            "mean"
        ),
        deals=("opportunity_id", "count")
    )
    .reset_index()
)

speed_summary_display = speed_summary.rename(
    columns={
        "deal_speed": "Deal speed",
        "response_rate": "Average response rate",
        "avg_response_time": "Average response time (hours)",
        "activity_count": "Average CRM activities per opportunity",
        "followup_count": "Average follow-ups per opportunity",
        "deals": "Closed opportunities",
    }
)

st.dataframe(
    speed_summary_display.style.format(
        {
            "Average response rate": "{:.1%}",
            "Average response time (hours)": "{:.1f}",
            "Average CRM activities per opportunity": "{:.1f}",
            "Average follow-ups per opportunity": "{:.1f}",
        }
    ),
    use_container_width=True
)


if len(closed_speed) > 0:

    fig_response = px.scatter(
        closed_speed,
        x="avg_response_time_hours",
        y="deal_duration_days",
        color="deal_speed",
        hover_data=[
            "opportunity_id",
            "sales_agent",
            "deal_stage"
        ],
        title="Response Time vs Deal Duration"
    )
    fig_response.update_xaxes(title="Average customer response time (hours)")
    fig_response.update_yaxes(title="Deal duration (days)")

    st.plotly_chart(
        fig_response,
        use_container_width=True
    )


# -----------------------------
# Sales agent performance
# -----------------------------

st.subheader("Sales Agent Performance")

agent_summary = (
    filtered.groupby("sales_agent")
    .agg(
        opportunities=("opportunity_id", "count"),
        avg_deal_duration=(
            "deal_duration_days",
            "mean"
        ),
        avg_response_rate=(
            "response_rate",
            "mean"
        ),
        avg_activity_count=(
            "activity_count",
            "mean"
        )
    )
    .reset_index()
)

agent_summary = agent_summary.sort_values(
    "avg_deal_duration"
)

agent_summary_display = agent_summary.rename(
    columns={
        "sales_agent": "Sales agent",
        "opportunities": "Opportunities",
        "avg_deal_duration": "Average deal duration (days)",
        "avg_response_rate": "Average response rate",
        "avg_activity_count": "Average CRM activities per opportunity",
    }
)

st.dataframe(
    agent_summary_display.head(15).style.format(
        {
            "Average deal duration (days)": "{:.1f}",
            "Average response rate": "{:.1%}",
            "Average CRM activities per opportunity": "{:.1f}",
        }
    ),
    use_container_width=True
)


# -----------------------------
# Product analysis
# -----------------------------

st.subheader("Deal Duration by Product")

product_summary = (
    closed.groupby("product")
    .agg(
        avg_duration=(
            "deal_duration_days",
            "mean"
        ),
        deals=(
            "opportunity_id",
            "count"
        )
    )
    .reset_index()
)

fig_product = px.bar(
    product_summary,
    x="product",
    y="avg_duration",
    title="Average Deal Duration by Product"
)

st.plotly_chart(
    fig_product,
    use_container_width=True
)


# -----------------------------
# Coaching insights
# -----------------------------

st.subheader("Coaching Signals")

if len(speed_summary) >= 2:

    fast = speed_summary[
        speed_summary["deal_speed"] == "Fast"
    ]

    slow = speed_summary[
        speed_summary["deal_speed"] == "Slow"
    ]

    if not fast.empty and not slow.empty:

        response_difference = (
            fast["response_rate"].iloc[0]
            - slow["response_rate"].iloc[0]
        )

        response_time_difference = (
            fast["avg_response_time"].iloc[0]
            - slow["avg_response_time"].iloc[0]
        )

        activity_difference = (
            fast["activity_count"].iloc[0]
            - slow["activity_count"].iloc[0]
        )

        st.write(
            f"- Fast deals show a "
            f"{response_difference:.1%} difference in "
            f"average response rate compared with slow deals."
        )

        st.write(
            f"- The difference in average response time "
            f"between fast and slow deals is "
            f"{abs(response_time_difference):.1f} hours."
        )

        st.write(
            f"- Fast deals average "
            f"{activity_difference:.1f} more CRM activities "
            f"than slow deals."
        )

st.warning(
    "Behavioural history is simulated for analytical "
    "prototyping. These signals should be treated as "
    "associations, not causal conclusions."
)
