"""Build one analytical row per sales opportunity without predictive ML."""

from pathlib import Path

import numpy as np
import pandas as pd

try:
    from .data_preparation import load_and_standardise
    from .numeric_analysis import iqr_outliers
except ImportError:
    from data_preparation import load_and_standardise
    from numeric_analysis import iqr_outliers


PROCESSED_DATA = Path("data/processed")
OUTPUT_PATH = PROCESSED_DATA / "opportunity_features.csv"


def create_pipeline_features(pipeline: pd.DataFrame) -> pd.DataFrame:
    pipeline = pipeline.copy()
    pipeline["is_closed"] = pipeline["deal_stage"].isin(["Won", "Lost"]).astype(int)
    pipeline["is_won"] = (pipeline["deal_stage"] == "Won").astype(int)
    pipeline["deal_duration_days"] = (pipeline["close_date"] - pipeline["engage_date"]).dt.days

    closed = pipeline["is_closed"].eq(1)
    duration = pipeline.loc[closed, "deal_duration_days"]
    lower, upper = duration.quantile([1 / 3, 2 / 3])
    pipeline["deal_speed"] = np.select(
        condlist=[
            closed & pipeline["deal_duration_days"].le(lower),
            closed & pipeline["deal_duration_days"].le(upper),
            closed,
        ],
        choicelist=["Fast", "Medium", "Slow"],
        default="Open",
    )

    won_close_value = pipeline["close_value"].where(pipeline["is_won"].eq(1))
    pipeline["is_close_value_outlier"] = iqr_outliers(won_close_value)
    return pipeline


def create_email_features(emails: pd.DataFrame) -> pd.DataFrame:
    if emails.empty:
        return pd.DataFrame(columns=[
            "opportunity_id", "email_count", "responded_email_count", "response_rate",
            "avg_response_time_hours", "median_response_time_hours",
        ])
    return (
        emails.assign(responded=emails["response_status"].eq("Responded").astype(int))
        .groupby("opportunity_id")
        .agg(
            email_count=("email_id", "count"),
            responded_email_count=("responded", "sum"),
            response_rate=("responded", "mean"),
            avg_response_time_hours=("response_time_hours", "mean"),
            median_response_time_hours=("response_time_hours", "median"),
        )
        .reset_index()
    )


def create_activity_features(activities: pd.DataFrame) -> pd.DataFrame:
    if activities.empty:
        return pd.DataFrame(columns=[
            "opportunity_id", "activity_count", "successful_activity_count",
            "unique_activity_types", "call_count", "meeting_count", "demo_count",
            "followup_count",
        ])
    activity = activities.copy()
    activity["successful_activity"] = activity["activity_outcome"].isin(
        {"Connected", "Completed", "Interested", "Responded"}
    ).astype(int)
    for column, activity_type in {
        "call_count": "Call", "meeting_count": "Meeting", "demo_count": "Demo", "followup_count": "Follow-up"
    }.items():
        activity[column] = activity["activity_type"].eq(activity_type).astype(int)
    return (
        activity.groupby("opportunity_id")
        .agg(
            activity_count=("activity_id", "count"),
            successful_activity_count=("successful_activity", "sum"),
            unique_activity_types=("activity_type", "nunique"),
            call_count=("call_count", "sum"), meeting_count=("meeting_count", "sum"),
            demo_count=("demo_count", "sum"), followup_count=("followup_count", "sum"),
        )
        .reset_index()
    )


def create_stage_features(stages: pd.DataFrame) -> pd.DataFrame:
    if stages.empty:
        return pd.DataFrame(columns=[
            "opportunity_id", "stage_transition_count", "total_stage_days", "avg_stage_days",
        ])
    return (
        stages.groupby("opportunity_id")
        .agg(
            stage_transition_count=("transition_id", "count"),
            total_stage_days=("days_in_previous_stage", "sum"),
            avg_stage_days=("days_in_previous_stage", "mean"),
        )
        .reset_index()
    )


def add_engagement_features(features: pd.DataFrame) -> pd.DataFrame:
    features = features.copy()
    numeric_zero_columns = [
        "email_count", "responded_email_count", "activity_count", "successful_activity_count",
        "unique_activity_types", "call_count", "meeting_count", "demo_count", "followup_count",
        "stage_transition_count", "total_stage_days",
    ]
    features[numeric_zero_columns] = features[numeric_zero_columns].fillna(0)
    features["has_behavioural_history"] = features["email_count"].gt(0).astype(int)

    active = features["has_behavioural_history"].eq(1)
    activity_median = features.loc[active, "activity_count"].median()
    high = active & features["response_rate"].ge(0.6) & features["activity_count"].ge(activity_median)
    medium = active & (features["response_rate"].ge(0.35) | features["activity_count"].ge(activity_median))
    features["engagement_level"] = np.select(
        condlist=[high, medium, active],
        choicelist=["High", "Medium", "Low"],
        default="No history",
    )
    return features


def build_feature_dataset(datasets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    features = create_pipeline_features(datasets["pipeline"])
    for aggregates in (
        create_email_features(datasets["emails"]),
        create_activity_features(datasets["activities"]),
        create_stage_features(datasets["stages"]),
    ):
        features = features.merge(aggregates, on="opportunity_id", how="left", validate="one_to_one")
    return add_engagement_features(features)


def main() -> None:
    features = build_feature_dataset(load_and_standardise())
    PROCESSED_DATA.mkdir(parents=True, exist_ok=True)
    features.to_csv(OUTPUT_PATH, index=False)
    print(f"Feature dataset created: {features.shape}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
