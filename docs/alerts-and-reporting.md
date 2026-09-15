# Alert Monitoring and Email Reporting

`src/email_report.py` adds two things to the dashboard: threshold-based alert
monitoring and an emailed HTML summary report. Both are descriptive - alerts
flag that a metric crossed a configured line, not that anything will happen
next.

## Alert Monitoring

`evaluate_alerts(data, thresholds)` checks the current filtered selection
against three configurable thresholds (defaults in `DEFAULT_THRESHOLDS`):

| Threshold | Default | Breached when |
|---|---|---|
| Minimum win rate | 40% | Win rate among closed deals falls below it |
| Minimum response rate | 30% | Average email response rate falls below it |
| Maximum average response time | 24 hours | Average response time rises above it |

Each breach is labelled `medium` or `high` severity based on how far past the
threshold the metric is (30% relative deviation is the cutoff for `high`).
The dashboard's "Alert Monitoring" section lets a manager adjust these
thresholds per session; they are not persisted between sessions.

## Email Reporting

The "Share This Report" section builds an HTML summary (`build_report_html`)
containing the current KPI snapshot and any active alerts, and sends it via
`send_email_report`.

Email credentials are read from environment variables and are never entered
into the dashboard or stored in the repository:

| Variable | Required | Purpose |
|---|---|---|
| `SMTP_HOST` | Yes | Mail server hostname |
| `SMTP_USERNAME` | Yes | SMTP login username |
| `SMTP_PASSWORD` | Yes | SMTP login password |
| `SMTP_PORT` | No (default `587`) | SMTP port |
| `SMTP_FROM` | No (defaults to `SMTP_USERNAME`) | From address |

If any required variable is missing, sending fails safely with a clear
message instead of raising an exception or crashing the app. The same is true
if the mail server rejects the connection or login - `send_email_report`
always returns `(success, message)` rather than letting an SMTP error
propagate.

## Run the tests

```bash
python -m unittest test_email_report -v
```

These tests never contact a real mail server: the "missing configuration"
path is exercised by clearing the environment, and the "server rejects
connection" path is exercised by mocking `smtplib.SMTP`.
