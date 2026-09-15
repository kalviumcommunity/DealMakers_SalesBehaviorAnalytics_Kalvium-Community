from io import BytesIO
import json
import unittest

from src.upload_processing import process_uploaded_dataset


PIPELINE = """opportunity_id,sales_agent,product,account,deal_stage,engage_date,close_date,close_value
A1,Agent One,Product,Account,Won,2026-01-01,2026-01-11,1000
A2,Agent One,Product,Account,Prospecting,2026-02-01,,
"""
EMAILS = """email_id,opportunity_id,sales_agent,sent_at,responded_at,response_time_hours,email_type,response_status
E1,A1,Agent One,2026-01-02 09:00,2026-01-02 12:00,3,Introduction,Responded
"""
ACTIVITIES = """activity_id,opportunity_id,sales_agent,activity_date,activity_type,activity_outcome
C1,A1,Agent One,2026-01-03 09:00,Call,Connected
"""
STAGES = """transition_id,opportunity_id,sales_agent,from_stage,to_stage,changed_at,days_in_previous_stage
S1,A1,Agent One,Prospecting,Engaging,2026-01-01,4
"""


def upload(text, name):
    value = BytesIO(text.encode())
    value.name = name
    return value


class UploadProcessingTests(unittest.TestCase):
    def test_pipeline_only_has_no_history(self):
        features, _ = process_uploaded_dataset({"sales_pipeline.csv": upload(PIPELINE, "sales_pipeline.csv")})
        prospect = features.loc[features["opportunity_id"] == "A2"].iloc[0]
        self.assertEqual(prospect["activity_count"], 0)
        self.assertEqual(prospect["stage_transition_count"], 0)
        self.assertEqual(prospect["engagement_level"], "No history")

    def test_full_upload_builds_features(self):
        files = {
            "sales_pipeline.csv": upload(PIPELINE, "sales_pipeline.csv"),
            "email_history.csv": upload(EMAILS, "email_history.csv"),
            "crm_activities.csv": upload(ACTIVITIES, "crm_activities.csv"),
            "stage_history.csv": upload(STAGES, "stage_history.csv"),
        }
        features, _ = process_uploaded_dataset(files)
        opportunity = features.loc[features["opportunity_id"] == "A1"].iloc[0]
        self.assertEqual(opportunity["email_count"], 1)
        self.assertEqual(opportunity["activity_count"], 1)
        self.assertEqual(opportunity["stage_transition_count"], 1)

    def assert_upload_rejected(self, pipeline, expected):
        with self.assertRaisesRegex(ValueError, expected):
            process_uploaded_dataset({"sales_pipeline.csv": upload(pipeline, "sales_pipeline.csv")})

    def test_invalid_stage_is_rejected(self):
        self.assert_upload_rejected(PIPELINE.replace("Prospecting", "Unknown"), "invalid deal stages")

    def test_lowercase_stage_is_normalised_not_rejected(self):
        lowercase = PIPELINE.replace("Won", "won").replace("Prospecting", "prospecting")
        features, _ = process_uploaded_dataset({"sales_pipeline.csv": upload(lowercase, "sales_pipeline.csv")})
        won_row = features.loc[features["opportunity_id"] == "A1"].iloc[0]
        self.assertEqual(won_row["deal_stage"], "Won")
        self.assertEqual(won_row["is_won"], 1)

    def test_whitespace_padded_stage_is_normalised(self):
        padded = PIPELINE.replace("Won", " Won  ")
        features, _ = process_uploaded_dataset({"sales_pipeline.csv": upload(padded, "sales_pipeline.csv")})
        won_row = features.loc[features["opportunity_id"] == "A1"].iloc[0]
        self.assertEqual(won_row["deal_stage"], "Won")

    def test_duplicate_opportunity_is_rejected(self):
        duplicate = PIPELINE + "A1,Agent One,Product,Account,Won,2026-01-01,2026-01-11,1000\n"
        self.assert_upload_rejected(duplicate, "duplicate opportunity_id")

    def test_invalid_date_is_rejected(self):
        self.assert_upload_rejected(PIPELINE.replace("2026-01-01", "not-a-date", 1), "invalid engage_date")

    def test_json_pipeline_upload_is_accepted(self):
        records = [
            {"opportunity_id": "A1", "sales_agent": "Agent One", "product": "Product", "account": "Account",
             "deal_stage": "Won", "engage_date": "2026-01-01", "close_date": "2026-01-11", "close_value": 1000},
            {"opportunity_id": "A2", "sales_agent": "Agent One", "product": "Product", "account": "Account",
             "deal_stage": "Prospecting", "engage_date": "2026-02-01", "close_date": None, "close_value": None},
        ]
        payload = json.dumps(records)
        features, _ = process_uploaded_dataset({"sales_pipeline.csv": upload(payload, "sales_pipeline.json")})
        self.assertEqual(len(features), 2)
        won_row = features.loc[features["opportunity_id"] == "A1"].iloc[0]
        self.assertEqual(won_row["is_won"], 1)

    def test_malformed_json_is_rejected_not_crashed(self):
        with self.assertRaisesRegex(ValueError, "could not read the JSON"):
            process_uploaded_dataset({"sales_pipeline.csv": upload("{not valid json", "sales_pipeline.json")})

    def test_unexpected_extension_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Expected sales_pipeline.csv or sales_pipeline.json"):
            process_uploaded_dataset({"sales_pipeline.csv": upload(PIPELINE, "sales_pipeline.txt")})

    def test_orphan_behavior_is_rejected(self):
        files = {
            "sales_pipeline.csv": upload(PIPELINE, "sales_pipeline.csv"),
            "email_history.csv": upload(EMAILS.replace("A1", "UNKNOWN"), "email_history.csv"),
        }
        with self.assertRaisesRegex(ValueError, "unknown opportunity_id"):
            process_uploaded_dataset(files)


if __name__ == "__main__":
    unittest.main()
