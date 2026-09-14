# Data Preparation and Quality Checks

## Purpose

`src/data_preparation.py` is the reproducible gateway from the raw CRM files to
the analytical pipeline. It standardises text fields, safely parses dates, and
validates the relationships and business rules that feature engineering relies
on. It does not delete records or fabricate missing values.

## Accepted source-data conditions

- Missing `account` values are retained because the source CRM does not provide
  an account for every opportunity.
- Prospecting opportunities can have no `engage_date` and no behavioural
  history.
- Open opportunities can have no `close_date` or `close_value`.
- Unanswered emails have no response timestamp or response-time value.

## Failing checks

The workflow fails when it detects duplicate primary keys, unknown deal stages,
incomplete closed deals, reversed dates, or behavioural rows that do not map to
a pipeline opportunity. Non-fatal timeline anomalies are reported as warnings.

## Run

```bash
.venv/bin/python src/data_preparation.py
```

This writes cleaned copies to `data/processed/cleaned/` and a machine-readable
report to `data/processed/data_quality_report.json`.

To validate without writing cleaned copies:

```bash
.venv/bin/python src/data_preparation.py --check-only
```

The feature-engineering stage (`src/feature_engineering.py`) consumes these
standardised datasets to build `data/processed/opportunity_features.csv` — see
[`docs/feature-engineering.md`](./feature-engineering.md).
