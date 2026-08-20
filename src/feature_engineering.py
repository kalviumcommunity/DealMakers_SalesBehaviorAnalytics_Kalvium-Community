"""Build one analytical row per sales opportunity without predictive ML."""

from pathlib import Path

import pandas as pd

from data_preparation import load_and_standardise


PROCESSED_DATA = Path("data/processed")
OUTPUT_PATH = PROCESSED_DATA / "opportunity_features.csv"


def create_pipeline_features(pipeline: pd.DataFrame) -> pd.DataFrame:
    pipeline = pipeline.copy()
    pipeline["is_closed"] = pipeline["deal_stage"].isin(["Won", "Lost"]).astype(int)
    pipeline["is_won"] = (pipeline["deal_stage"] == "Won").astype(int)
    pipeline["deal_duration_days"] = (pipeline["close_date"] - pipeline["engage_date"]).dt.days
    pipeline["deal_speed"] = "Open"
    duration = pipeline.loc[pipeline["is_closed"].eq(1), "deal_duration_days"]
    lower, upper = duration.quantile([1 / 3, 2 / 3])
    closed = pipeline["is_closed"].eq(1)
    pipeline.loc[closed & pipeline["deal_duration_days"].le(lower), "deal_speed"] = "Fast"
    pipeline.loc[closed & pipeline["deal_duration_days"].gt(lower) & pipeline["deal_duration_days"].le(upper), "deal_speed"] = "Medium"
    pipeline.loc[closed & pipeline["deal_duration_days"].gt(upper), "deal_speed"] = "Slow"
    return pipeline


def create_email_features(emails: pd.DataFrame) -> pd.DataFrame:
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
    features["engagement_level"] = "No history"
    features.loc[active, "engagement_level"] = "Low"
    features.loc[active & features["response_rate"].ge(0.6) & features["activity_count"].ge(activity_median), "engagement_level"] = "High"
    features.loc[
        active & features["engagement_level"].ne("High")
        & (features["response_rate"].ge(0.35) | features["activity_count"].ge(activity_median)),
        "engagement_level",
    ] = "Medium"
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
