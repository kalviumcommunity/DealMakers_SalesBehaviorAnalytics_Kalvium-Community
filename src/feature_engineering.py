import pandas as pd
from pathlib import Path


RAW_DATA = Path("data/raw")
PROCESSED_DATA = Path("data/processed")


def load_data():
    pipeline = pd.read_csv(RAW_DATA / "sales_pipeline.csv")
    emails = pd.read_csv(RAW_DATA / "email_history.csv")
    activities = pd.read_csv(RAW_DATA / "crm_activities.csv")
    stages = pd.read_csv(RAW_DATA / "stage_history.csv")

    return pipeline, emails, activities, stages


def create_email_features(emails):
    email_features = (
        emails.groupby("opportunity_id")
        .agg(
            email_count=("email_id", "count"),
            response_rate=(
                "response_status",
                lambda x: (x == "Responded").mean()
            ),
            avg_response_hours=("response_time_hours", "mean"),
            median_response_hours=("response_time_hours", "median"),
        )
        .reset_index()
    )

    return email_features


def create_activity_features(activities):
    activity_features = (
        activities.groupby("opportunity_id")
        .agg(
            activity_count=("activity_id", "count"),
            unique_activity_types=("activity_type", "nunique"),
        )
        .reset_index()
    )

    return activity_features


def create_stage_features(stages):
    stage_features = (
        stages.groupby("opportunity_id")
        .agg(
            stage_transition_count=("transition_id", "count"),
            total_stage_days=("days_in_previous_stage", "sum"),
            avg_stage_days=("days_in_previous_stage", "mean"),
        )
        .reset_index()
    )

    return stage_features


def create_pipeline_features(pipeline):
    pipeline = pipeline.copy()

    pipeline["engage_date"] = pd.to_datetime(
        pipeline["engage_date"],
        errors="coerce"
    )

    pipeline["close_date"] = pd.to_datetime(
        pipeline["close_date"],
        errors="coerce"
    )

    pipeline["deal_duration_days"] = (
        pipeline["close_date"] - pipeline["engage_date"]
    ).dt.days

    return pipeline


def build_feature_dataset(
    pipeline,
    email_features,
    activity_features,
    stage_features
):
    features = pipeline.merge(
        email_features,
        on="opportunity_id",
        how="left"
    )

    features = features.merge(
        activity_features,
        on="opportunity_id",
        how="left"
    )

    features = features.merge(
        stage_features,
        on="opportunity_id",
        how="left"
    )

    return features


def main():
    print("Loading datasets...")

    pipeline, emails, activities, stages = load_data()

    print("Creating pipeline features...")
    pipeline = create_pipeline_features(pipeline)

    print("Creating email features...")
    email_features = create_email_features(emails)

    print("Creating activity features...")
    activity_features = create_activity_features(activities)

    print("Creating stage features...")
    stage_features = create_stage_features(stages)

    print("Combining datasets...")

    features = build_feature_dataset(
        pipeline,
        email_features,
        activity_features,
        stage_features
    )

    PROCESSED_DATA.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = (
        PROCESSED_DATA / "opportunity_features.csv"
    )

    features.to_csv(
        output_path,
        index=False
    )

    print("\nFeature dataset created:")
    print(features.shape)

    print("\nColumns:")
    print(features.columns.tolist())

    print("\nSaved to:")
    print(output_path)


if __name__ == "__main__":
    main()