import os
import unittest
from unittest.mock import patch

import pandas as pd

from src.email_report import (
    DEFAULT_THRESHOLDS,
    build_report_html,
    evaluate_alerts,
    send_email_report,
)


def _data(win_rate_pct, response_rate_pct, avg_response_time_hours):
    won = int(win_rate_pct)
    lost = 100 - won
    rows = (
        [{"is_closed": 1, "is_won": 1, "response_rate": response_rate_pct / 100, "avg_response_time_hours": avg_response_time_hours}] * won
        + [{"is_closed": 1, "is_won": 0, "response_rate": response_rate_pct / 100, "avg_response_time_hours": avg_response_time_hours}] * lost
    )
    return pd.DataFrame(rows)


class EvaluateAlertsTests(unittest.TestCase):
    def test_no_alerts_when_metrics_are_healthy(self):
        data = _data(win_rate_pct=60, response_rate_pct=50, avg_response_time_hours=10)
        self.assertEqual(evaluate_alerts(data, DEFAULT_THRESHOLDS), [])

    def test_low_win_rate_triggers_alert(self):
        data = _data(win_rate_pct=10, response_rate_pct=50, avg_response_time_hours=10)
        alerts = evaluate_alerts(data, DEFAULT_THRESHOLDS)
        metrics = [alert["metric"] for alert in alerts]
        self.assertIn("Win Rate", metrics)

    def test_severely_low_win_rate_is_high_severity(self):
        data = _data(win_rate_pct=5, response_rate_pct=50, avg_response_time_hours=10)
        alerts = evaluate_alerts(data, DEFAULT_THRESHOLDS)
        win_rate_alert = next(alert for alert in alerts if alert["metric"] == "Win Rate")
        self.assertEqual(win_rate_alert["severity"], "high")

    def test_slightly_low_win_rate_is_medium_severity(self):
        data = _data(win_rate_pct=38, response_rate_pct=50, avg_response_time_hours=10)
        alerts = evaluate_alerts(data, DEFAULT_THRESHOLDS)
        win_rate_alert = next(alert for alert in alerts if alert["metric"] == "Win Rate")
        self.assertEqual(win_rate_alert["severity"], "medium")

    def test_slow_response_time_triggers_alert(self):
        data = _data(win_rate_pct=60, response_rate_pct=50, avg_response_time_hours=48)
        alerts = evaluate_alerts(data, DEFAULT_THRESHOLDS)
        self.assertIn("Average Response Time", [alert["metric"] for alert in alerts])

    def test_empty_data_has_no_alerts(self):
        self.assertEqual(evaluate_alerts(pd.DataFrame(), DEFAULT_THRESHOLDS), [])


class BuildReportHtmlTests(unittest.TestCase):
    def test_report_includes_metrics_and_alert_messages(self):
        alerts = [{"metric": "Win Rate", "value": "10.0%", "threshold": "40.0%", "severity": "high", "message": "Win rate is 10.0%, below the 40.0% target."}]
        html = build_report_html("Demo Dataset", {"Opportunities": "8,300"}, alerts)
        self.assertIn("Demo Dataset", html)
        self.assertIn("8,300", html)
        self.assertIn("Win rate is 10.0%", html)

    def test_report_notes_no_breaches_when_no_alerts(self):
        html = build_report_html("Demo Dataset", {"Opportunities": "8,300"}, [])
        self.assertIn("No thresholds were breached", html)


class SendEmailReportTests(unittest.TestCase):
    def test_missing_configuration_fails_safely_without_network(self):
        with patch.dict(os.environ, {}, clear=True):
            success, message = send_email_report("manager@example.com", "Weekly Report", "<p>hi</p>")
        self.assertFalse(success)
        self.assertIn("not configured", message)

    def test_smtp_failure_is_caught_and_reported(self):
        env = {"SMTP_HOST": "smtp.example.com", "SMTP_USERNAME": "user", "SMTP_PASSWORD": "pass"}
        with patch.dict(os.environ, env, clear=True), patch("smtplib.SMTP", side_effect=OSError("connection refused")):
            success, message = send_email_report("manager@example.com", "Weekly Report", "<p>hi</p>")
        self.assertFalse(success)
        self.assertIn("Failed to send email", message)

    def test_successful_send_reports_recipient(self):
        env = {"SMTP_HOST": "smtp.example.com", "SMTP_USERNAME": "user", "SMTP_PASSWORD": "pass"}
        with patch.dict(os.environ, env, clear=True), patch("smtplib.SMTP") as smtp_class:
            smtp_class.return_value.__enter__.return_value = smtp_class.return_value
            success, message = send_email_report("manager@example.com", "Weekly Report", "<p>hi</p>")
        self.assertTrue(success)
        self.assertIn("manager@example.com", message)


if __name__ == "__main__":
    unittest.main()
