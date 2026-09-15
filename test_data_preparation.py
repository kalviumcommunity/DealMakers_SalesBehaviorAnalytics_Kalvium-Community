import unittest

import pandas as pd

from src.data_preparation import validate_datasets


def _pipeline(rows):
    defaults = {
        "opportunity_id": None, "sales_agent": "Agent One", "product": "Product",
        "account": "Account", "deal_stage": "Won",
        "engage_date": pd.Timestamp("2026-01-01"), "close_date": pd.Timestamp("2026-01-11"),
        "close_value": 1000,
    }
    return pd.DataFrame([{**defaults, **row} for row in rows])


def _empty(columns):
    return pd.DataFrame(columns=columns)


EMPTY_EMAILS = _empty(["email_id", "opportunity_id", "sent_at", "responded_at", "response_time_hours", "response_status"])
EMPTY_ACTIVITIES = _empty(["activity_id", "opportunity_id", "activity_date"])
EMPTY_STAGES = _empty(["transition_id", "opportunity_id", "days_in_previous_stage"])


def _datasets(pipeline):
    return {"pipeline": pipeline, "emails": EMPTY_EMAILS, "activities": EMPTY_ACTIVITIES, "stages": EMPTY_STAGES}


def _status(findings, check):
    return next(item["status"] for item in findings if item["check"] == check)


class NearDuplicateDetectionTests(unittest.TestCase):
    def test_no_warning_for_distinct_opportunities(self):
        pipeline = _pipeline([
            {"opportunity_id": "A1", "close_value": 1000},
            {"opportunity_id": "A2", "close_value": 2000},
        ])
        findings = validate_datasets(_datasets(pipeline))
        self.assertEqual(_status(findings, "near_duplicate_opportunities"), "pass")

    def test_warns_when_account_product_date_and_value_all_match(self):
        pipeline = _pipeline([
            {"opportunity_id": "A1", "close_value": 1000},
            {"opportunity_id": "A2", "close_value": 1000},
        ])
        findings = validate_datasets(_datasets(pipeline))
        finding = next(item for item in findings if item["check"] == "near_duplicate_opportunities")
        self.assertEqual(finding["status"], "warning")
        self.assertIn("2 opportunities", finding["detail"])

    def test_rows_missing_a_key_field_are_not_compared(self):
        pipeline = _pipeline([
            {"opportunity_id": "A1", "close_value": 1000},
            {"opportunity_id": "A2", "close_value": None},
        ])
        findings = validate_datasets(_datasets(pipeline))
        self.assertEqual(_status(findings, "near_duplicate_opportunities"), "pass")

    def test_does_not_flag_valid_data_as_a_hard_failure(self):
        pipeline = _pipeline([
            {"opportunity_id": "A1", "close_value": 1000},
            {"opportunity_id": "A2", "close_value": 1000},
        ])
        findings = validate_datasets(_datasets(pipeline))
        statuses = {item["status"] for item in findings}
        self.assertNotIn("fail", statuses)


if __name__ == "__main__":
    unittest.main()
