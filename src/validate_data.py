import pandas as pd


PIPELINE = "data/raw/sales_pipeline.csv"
EMAILS = "data/raw/email_history.csv"
ACTIVITIES = "data/raw/crm_activities.csv"
STAGES = "data/raw/stage_history.csv"


def main():

    pipeline = pd.read_csv(PIPELINE)
    emails = pd.read_csv(EMAILS)
    activities = pd.read_csv(ACTIVITIES)
    stages = pd.read_csv(STAGES)

    print("=== DATASET SIZES ===")

    print("Pipeline:", pipeline.shape)
    print("Emails:", emails.shape)
    print("Activities:", activities.shape)
    print("Stage history:", stages.shape)

    print("\n=== EMAIL RESPONSE RATE ===")

    response_rate = (
        emails["response_status"] == "Responded"
    ).mean() * 100

    print(f"{response_rate:.2f}%")

    print("\n=== EMAIL RESPONSE BY DEAL STAGE ===")

    email_counts = (
        emails.groupby("opportunity_id")
        .size()
        .rename("email_count")
    )

    response_rates = (
        emails.groupby("opportunity_id")["response_status"]
        .apply(lambda x: (x == "Responded").mean())
        .rename("response_rate")
    )

    analysis = pipeline.merge(
        email_counts,
        on="opportunity_id",
        how="left"
    )

    analysis = analysis.merge(
        response_rates,
        on="opportunity_id",
        how="left"
    )

    print(
        analysis.groupby("deal_stage")
        [["email_count", "response_rate"]]
        .mean()
    )

    print("\n=== ACTIVITY BY DEAL STAGE ===")

    activity_counts = (
        activities.groupby("opportunity_id")
        .size()
        .rename("activity_count")
    )

    analysis = analysis.merge(
        activity_counts,
        on="opportunity_id",
        how="left"
    )

    print(
        analysis.groupby("deal_stage")
        ["activity_count"]
        .mean()
    )

    print("\n=== MISSING VALUES ===")

    print("Pipeline:")
    print(pipeline.isnull().sum())

    print("\nEmails:")
    print(emails.isnull().sum())

    print("\nActivities:")
    print(activities.isnull().sum())

    print("\n=== VALIDATION ===")

    print(
        "Pipeline opportunity IDs:",
        pipeline["opportunity_id"].nunique()
    )

    print(
        "Email opportunity IDs:",
        emails["opportunity_id"].nunique()
    )

    print(
        "Activity opportunity IDs:",
        activities["opportunity_id"].nunique()
    )


if __name__ == "__main__":
    main()