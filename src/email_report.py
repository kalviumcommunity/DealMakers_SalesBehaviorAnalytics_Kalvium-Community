"""Threshold alert evaluation and email report delivery.

Alerts are descriptive threshold checks against dashboard KPIs, not
predictions. Email credentials are read from environment variables only -
never hardcoded or entered into the dashboard - and sending failures are
caught so a missing or misconfigured mail server never crashes the app.
"""

from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage

import pandas as pd

DEFAULT_THRESHOLDS = {
    "min_win_rate": 40.0,
    "min_response_rate": 30.0,
    "max_avg_response_time_hours": 24.0,
}


def _severity(deviation_ratio: float) -> str:
    """deviation_ratio is how far past the threshold the metric is, as a fraction."""
    return "high" if deviation_ratio >= 0.3 else "medium"


def evaluate_alerts(data: pd.DataFrame, thresholds: dict[str, float]) -> list[dict[str, str]]:
    """Return a list of {metric, value, threshold, severity, message} for breached thresholds."""
    alerts: list[dict[str, str]] = []
    if data.empty:
        return alerts

    closed = data[data["is_closed"] == 1]
    won = data[data["is_won"] == 1]

    if len(closed):
        win_rate = len(won) / len(closed) * 100
        min_win_rate = thresholds["min_win_rate"]
        if win_rate < min_win_rate:
            deviation = (min_win_rate - win_rate) / min_win_rate
            alerts.append({
                "metric": "Win Rate", "value": f"{win_rate:.1f}%", "threshold": f"{min_win_rate:.1f}%",
                "severity": _severity(deviation),
                "message": f"Win rate is {win_rate:.1f}%, below the {min_win_rate:.1f}% target.",
            })

    if data["response_rate"].notna().any():
        avg_response_rate = data["response_rate"].mean() * 100
        min_response_rate = thresholds["min_response_rate"]
        if avg_response_rate < min_response_rate:
            deviation = (min_response_rate - avg_response_rate) / min_response_rate
            alerts.append({
                "metric": "Average Response Rate", "value": f"{avg_response_rate:.1f}%",
                "threshold": f"{min_response_rate:.1f}%", "severity": _severity(deviation),
                "message": f"Average response rate is {avg_response_rate:.1f}%, below the {min_response_rate:.1f}% target.",
            })

    if data["avg_response_time_hours"].notna().any():
        avg_response_time = data["avg_response_time_hours"].mean()
        max_response_time = thresholds["max_avg_response_time_hours"]
        if avg_response_time > max_response_time:
            deviation = (avg_response_time - max_response_time) / max_response_time
            alerts.append({
                "metric": "Average Response Time", "value": f"{avg_response_time:.1f}h",
                "threshold": f"{max_response_time:.1f}h", "severity": _severity(deviation),
                "message": f"Average response time is {avg_response_time:.1f} hours, above the {max_response_time:.1f}-hour target.",
            })

    return alerts


def build_report_html(dataset_label: str, metrics: dict[str, str], alerts: list[dict[str, str]]) -> str:
    """Build a self-contained HTML report: a KPI section and an alerts section."""
    metric_rows = "".join(
        f"<tr><td style='padding:4px 12px;'>{name}</td><td style='padding:4px 12px;'><b>{value}</b></td></tr>"
        for name, value in metrics.items()
    )
    if alerts:
        severity_color = {"high": "#c0392b", "medium": "#d68910"}
        alert_rows = "".join(
            f"<li style='color:{severity_color.get(alert['severity'], '#333')};'>"
            f"<b>[{alert['severity'].upper()}]</b> {alert['message']}</li>"
            for alert in alerts
        )
        alerts_html = f"<ul>{alert_rows}</ul>"
    else:
        alerts_html = "<p>No thresholds were breached for this selection.</p>"

    return f"""
    <html><body>
    <h2>Sales Behaviour Analytics - {dataset_label}</h2>
    <h3>Key Metrics</h3>
    <table>{metric_rows}</table>
    <h3>Alerts</h3>
    {alerts_html}
    <p style="color:#666; font-size:12px;">
        Behavioural history may be simulated. These figures are descriptive
        associations, not predictions or causal conclusions.
    </p>
    </body></html>
    """


def send_email_report(recipient: str, subject: str, html_body: str) -> tuple[bool, str]:
    """Send an HTML email using SMTP credentials from the environment.

    Returns (success, message) instead of raising, so a missing or failing
    mail server never crashes the caller.
    """
    host = os.environ.get("SMTP_HOST")
    port = os.environ.get("SMTP_PORT", "587")
    username = os.environ.get("SMTP_USERNAME")
    password = os.environ.get("SMTP_PASSWORD")
    sender = os.environ.get("SMTP_FROM", username)

    if not all([host, username, password]):
        return False, (
            "Email is not configured. Set the SMTP_HOST, SMTP_USERNAME, and "
            "SMTP_PASSWORD environment variables (and optionally SMTP_PORT, "
            "SMTP_FROM) to enable sending."
        )

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient
    message.set_content("This report requires an HTML-capable email client.")
    message.add_alternative(html_body, subtype="html")

    try:
        with smtplib.SMTP(host, int(port), timeout=10) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(message)
    except (smtplib.SMTPException, OSError) as error:
        return False, f"Failed to send email: {error}"

    return True, f"Report emailed to {recipient}."
