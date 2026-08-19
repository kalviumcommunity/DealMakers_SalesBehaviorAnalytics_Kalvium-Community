import random
from datetime import timedelta

import pandas as pd


RANDOM_SEED = 42

def create_behaviour_profile(deal):
    """
    Create a behavioural tendency for one opportunity.

    Behaviour varies naturally across opportunities.
    The generated behaviour is later compared with the
    actual CRM outcome and deal duration.
    """

    behaviour_type = random.choice([
        "high_engagement",
        "moderate_engagement",
        "low_engagement"
    ])

    if behaviour_type == "high_engagement":
        profile = {
            "response_probability": random.uniform(0.70, 0.90),
            "min_response_hours": 2,
            "max_response_hours": 24,
            "activity_min": 6,
            "activity_max": 10,
        }

    elif behaviour_type == "moderate_engagement":
        profile = {
            "response_probability": random.uniform(0.45, 0.70),
            "min_response_hours": 12,
            "max_response_hours": 60,
            "activity_min": 4,
            "activity_max": 8,
        }

    else:
        profile = {
            "response_probability": random.uniform(0.25, 0.50),
            "min_response_hours": 24,
            "max_response_hours": 96,
            "activity_min": 2,
            "activity_max": 6,
        }

    return profile


def load_pipeline():
    return pd.read_csv("data/raw/sales_pipeline.csv")


def prepare_dates(pipeline):
    pipeline["engage_date"] = pd.to_datetime(pipeline["engage_date"])
    pipeline["close_date"] = pd.to_datetime(pipeline["close_date"])

    return pipeline


def generate_stage_history(pipeline):
    stage_records = []

    for _, deal in pipeline.iterrows():

        opportunity_id = deal["opportunity_id"]
        sales_agent = deal["sales_agent"]
        deal_stage = deal["deal_stage"]
        engage_date = deal["engage_date"]
        close_date = deal["close_date"]

        # Deals that have reached Engaging
        if pd.notna(engage_date):

            # Simulate Prospecting -> Engaging transition
            prospecting_days = random.randint(3, 30)

            prospecting_date = (
                engage_date - timedelta(days=prospecting_days)
            )

            stage_records.append({
                "transition_id": f"ST-{len(stage_records) + 1:06d}",
                "opportunity_id": opportunity_id,
                "sales_agent": sales_agent,
                "from_stage": "Prospecting",
                "to_stage": "Engaging",
                "changed_at": engage_date,
                "days_in_previous_stage": prospecting_days
            })

            # Closed opportunities
            if deal_stage in ["Won", "Lost"] and pd.notna(close_date):

                engaging_days = (close_date - engage_date).days

                stage_records.append({
                    "transition_id": f"ST-{len(stage_records) + 1:06d}",
                    "opportunity_id": opportunity_id,
                    "sales_agent": sales_agent,
                    "from_stage": "Engaging",
                    "to_stage": deal_stage,
                    "changed_at": close_date,
                    "days_in_previous_stage": engaging_days
                })

    return pd.DataFrame(stage_records)


def generate_email_history(pipeline):
    email_records = []

    email_types = [
        "Introduction",
        "Follow-up",
        "Proposal",
        "Product information",
        "Negotiation",
        "Closing follow-up"
    ]

    for _, deal in pipeline.iterrows():

        opportunity_id = deal["opportunity_id"]
        sales_agent = deal["sales_agent"]
        engage_date = deal["engage_date"]
        close_date = deal["close_date"]

        if pd.isna(engage_date):
            continue

        profile = create_behaviour_profile(deal)

        if pd.notna(close_date):
            end_date = close_date
        else:
            end_date = engage_date + timedelta(days=30)

        total_days = max((end_date - engage_date).days, 1)

        number_of_emails = random.randint(
            profile["activity_min"],
            min(profile["activity_max"], 8)
        )

        for _ in range(number_of_emails):

            sent_offset = random.randint(0, total_days)

            sent_at = engage_date + timedelta(
                days=sent_offset,
                hours=random.randint(8, 17)
            )

            responded = (
                random.random()
                < profile["response_probability"]
            )

            if responded:

                response_hours = random.randint(
                    profile["min_response_hours"],
                    profile["max_response_hours"]
                )

                responded_at = sent_at + timedelta(
                    hours=response_hours
                )

                if responded_at > end_date:
                    responded_at = pd.NaT

                if pd.notna(responded_at):
                    actual_response_hours = (
                        responded_at - sent_at
                    ).total_seconds() / 3600
                else:
                    actual_response_hours = None

            else:
                responded_at = pd.NaT
                actual_response_hours = None

            email_records.append({
                "email_id": f"EM-{len(email_records) + 1:06d}",
                "opportunity_id": opportunity_id,
                "sales_agent": sales_agent,
                "sent_at": sent_at,
                "responded_at": responded_at,
                "response_time_hours": actual_response_hours,
                "email_type": random.choice(email_types),
                "response_status":
                    "Responded"
                    if pd.notna(responded_at)
                    else "No Response"
            })

    return pd.DataFrame(email_records)


def generate_crm_activities(pipeline):
    activity_records = []

    activity_types = [
        "Call",
        "Email",
        "Meeting",
        "Demo",
        "Follow-up"
    ]

    outcomes = [
        "Connected",
        "No answer",
        "Completed",
        "Rescheduled",
        "Interested",
        "Not interested",
        "Responded"
    ]

    for _, deal in pipeline.iterrows():

        opportunity_id = deal["opportunity_id"]
        sales_agent = deal["sales_agent"]
        engage_date = deal["engage_date"]
        close_date = deal["close_date"]

        if pd.isna(engage_date):
            continue

        profile = create_behaviour_profile(deal)

        if pd.notna(close_date):
            end_date = close_date
        else:
            end_date = engage_date + timedelta(days=30)

        total_days = max((end_date - engage_date).days, 1)

        number_of_activities = random.randint(
            profile["activity_min"],
            profile["activity_max"]
        )

        for _ in range(number_of_activities):

            activity_offset = random.randint(0, total_days)

            activity_date = (
                engage_date
                + timedelta(
                    days=activity_offset,
                    hours=random.randint(8, 17)
                )
            )

            activity_records.append({
                "activity_id": f"ACT-{len(activity_records) + 1:06d}",
                "opportunity_id": opportunity_id,
                "sales_agent": sales_agent,
                "activity_date": activity_date,
                "activity_type": random.choice(activity_types),
                "activity_outcome": random.choice(outcomes)
            })

    return pd.DataFrame(activity_records)


def main():

    random.seed(RANDOM_SEED)

    pipeline = load_pipeline()
    pipeline = prepare_dates(pipeline)

    print("Generating stage history...")
    stage_history = generate_stage_history(pipeline)

    print("Generating email history...")
    email_history = generate_email_history(pipeline)

    print("Generating CRM activities...")
    crm_activities = generate_crm_activities(pipeline)

    stage_history.to_csv(
        "data/raw/stage_history.csv",
        index=False
    )

    email_history.to_csv(
        "data/raw/email_history.csv",
        index=False
    )

    crm_activities.to_csv(
        "data/raw/crm_activities.csv",
        index=False
    )

    print("\nGenerated datasets:")

    print(
        "stage_history:",
        stage_history.shape
    )

    print(
        "email_history:",
        email_history.shape
    )

    print(
        "crm_activities:",
        crm_activities.shape
    )


if __name__ == "__main__":
    main()
