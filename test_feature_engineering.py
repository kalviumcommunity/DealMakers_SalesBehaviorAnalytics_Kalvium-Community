import unittest

import pandas as pd

from src.feature_engineering import (
    add_engagement_features,
    build_feature_dataset,
    create_activity_features,
    create_email_features,
    create_pipeline_features,
    create_stage_features,
)


def _pipeline_frame():
    return pd.DataFrame({
        "opportunity_id": ["A1", "A2", "A3", "A4"],
        "sales_agent": ["Agent One"] * 4,
        "product": ["Product"] * 4,
        "account": ["Account"] * 4,
        "deal_stage": ["Won", "Lost", "Won", "Prospecting"],
        "engage_date": pd.to_datetime(["2026-01-01", "2026-01-01", "2026-01-01", "2026-02-01"]),
        "close_date": pd.to_datetime(["2026-01-06", "2026-01-21", "2026-01-11", pd.NaT]),
        "close_value": [1000, 0, 2000, None],
    })


class CreatePipelineFeaturesTests(unittest.TestCase):
    def test_closed_and_won_flags(self):
        features = create_pipeline_features(_pipeline_frame())
        flags = features.set_index("opportunity_id")[["is_closed", "is_won"]]
        self.assertEqual(flags.loc["A1"].tolist(), [1, 1])
        self.assertEqual(flags.loc["A2"].tolist(), [1, 0])
        self.assertEqual(flags.loc["A4"].tolist(), [0, 0])

    def test_deal_duration_only_for_closed(self):
        features = create_pipeline_features(_pipeline_frame())
        durations = features.set_index("opportunity_id")["deal_duration_days"]
        self.assertEqual(durations["A1"], 5)
        self.assertEqual(durations["A2"], 20)
        self.assertTrue(pd.isna(durations["A4"]))

    def test_open_deal_has_open_speed(self):
        features = create_pipeline_features(_pipeline_frame())
        speed = features.set_index("opportunity_id")["deal_speed"]
        self.assertEqual(speed["A4"], "Open")
        self.assertIn(speed["A1"], {"Fast", "Medium", "Slow"})


class CreateEmailFeaturesTests(unittest.TestCase):
    def test_empty_emails_return_expected_columns(self):
        result = create_email_features(pd.DataFrame())
        self.assertEqual(len(result), 0)
        self.assertIn("response_rate", result.columns)

    def test_response_rate_and_timing(self):
        emails = pd.DataFrame({
            "email_id": ["E1", "E2"],
            "opportunity_id": ["A1", "A1"],
            "response_status": ["Responded", "No Response"],
            "response_time_hours": [4, None],
        })
        result = create_email_features(emails).set_index("opportunity_id").loc["A1"]
        self.assertEqual(result["email_count"], 2)
        self.assertEqual(result["responded_email_count"], 1)
        self.assertEqual(result["response_rate"], 0.5)
        self.assertEqual(result["avg_response_time_hours"], 4)


class CreateActivityFeaturesTests(unittest.TestCase):
    def test_empty_activities_return_expected_columns(self):
        result = create_activity_features(pd.DataFrame())
        self.assertEqual(len(result), 0)
        self.assertIn("call_count", result.columns)

    def test_counts_by_type_and_outcome(self):
        activities = pd.DataFrame({
            "activity_id": ["C1", "C2", "C3"],
            "opportunity_id": ["A1", "A1", "A1"],
            "activity_type": ["Call", "Demo", "Call"],
            "activity_outcome": ["Connected", "No Show", "Connected"],
        })
        result = create_activity_features(activities).set_index("opportunity_id").loc["A1"]
        self.assertEqual(result["activity_count"], 3)
        self.assertEqual(result["successful_activity_count"], 2)
        self.assertEqual(result["call_count"], 2)
        self.assertEqual(result["demo_count"], 1)
        self.assertEqual(result["unique_activity_types"], 2)


class CreateStageFeaturesTests(unittest.TestCase):
    def test_empty_stages_return_expected_columns(self):
        result = create_stage_features(pd.DataFrame())
        self.assertEqual(len(result), 0)
        self.assertIn("stage_transition_count", result.columns)

    def test_transition_and_day_aggregates(self):
        stages = pd.DataFrame({
            "transition_id": ["S1", "S2"],
            "opportunity_id": ["A1", "A1"],
            "days_in_previous_stage": [4, 6],
        })
        result = create_stage_features(stages).set_index("opportunity_id").loc["A1"]
        self.assertEqual(result["stage_transition_count"], 2)
        self.assertEqual(result["total_stage_days"], 10)
        self.assertEqual(result["avg_stage_days"], 5)


class AddEngagementFeaturesTests(unittest.TestCase):
    def test_no_history_when_no_emails(self):
        features = pd.DataFrame({
            "opportunity_id": ["A1"],
            "email_count": [0], "responded_email_count": [0], "response_rate": [None],
            "activity_count": [0], "successful_activity_count": [0], "unique_activity_types": [0],
            "call_count": [0], "meeting_count": [0], "demo_count": [0], "followup_count": [0],
            "stage_transition_count": [0], "total_stage_days": [0],
        })
        result = add_engagement_features(features)
        self.assertEqual(result.loc[0, "has_behavioural_history"], 0)
        self.assertEqual(result.loc[0, "engagement_level"], "No history")

    def test_high_engagement_requires_response_and_activity(self):
        features = pd.DataFrame({
            "opportunity_id": ["A1", "A2"],
            "email_count": [5, 5], "responded_email_count": [4, 1], "response_rate": [0.8, 0.2],
            "activity_count": [10, 1], "successful_activity_count": [5, 0], "unique_activity_types": [2, 1],
            "call_count": [3, 1], "meeting_count": [1, 0], "demo_count": [1, 0], "followup_count": [1, 0],
            "stage_transition_count": [2, 1], "total_stage_days": [10, 5],
        })
        result = add_engagement_features(features).set_index("opportunity_id")
        self.assertEqual(result.loc["A1", "engagement_level"], "High")
        self.assertEqual(result.loc["A2", "engagement_level"], "Low")


class BuildFeatureDatasetTests(unittest.TestCase):
    def test_combines_all_sources_into_one_row_per_opportunity(self):
        datasets = {
            "pipeline": _pipeline_frame(),
            "emails": pd.DataFrame({
                "email_id": ["E1"], "opportunity_id": ["A1"],
                "response_status": ["Responded"], "response_time_hours": [3],
            }),
            "activities": pd.DataFrame({
                "activity_id": ["C1"], "opportunity_id": ["A1"],
                "activity_type": ["Call"], "activity_outcome": ["Connected"],
            }),
            "stages": pd.DataFrame({
                "transition_id": ["S1"], "opportunity_id": ["A1"], "days_in_previous_stage": [4],
            }),
        }
        features = build_feature_dataset(datasets)
        self.assertEqual(len(features), 4)
        a1 = features.set_index("opportunity_id").loc["A1"]
        self.assertEqual(a1["email_count"], 1)
        self.assertEqual(a1["activity_count"], 1)
        self.assertEqual(a1["stage_transition_count"], 1)
        a4 = features.set_index("opportunity_id").loc["A4"]
        self.assertEqual(a4["engagement_level"], "No history")


if __name__ == "__main__":
    unittest.main()
