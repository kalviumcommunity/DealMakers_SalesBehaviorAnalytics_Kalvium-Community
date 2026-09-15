# Data Preparation and Quality Checks

## Purpose

`src/data_preparation.py` is the reproducible gateway from the raw CRM files to
the analytical pipeline. It standardises text fields, safely parses dates, and
validates the relationships and business rules that feature engineering relies
on. It does not delete records or fabricate missing values - missing values
are detected and reported, never imputed, so the pipeline never presents a
guessed number as if it were observed data.

## Type enforcement

All ID columns (`opportunity_id`, `email_id`, `activity_id`, `transition_id`)
are cast to string, and all monetary/duration numeric columns (`close_value`,
`response_time_hours`, `days_in_previous_stage`) are cast to numeric,
explicitly - not left as whatever pandas happened to infer from the CSV. This
matters because an ID that looks numeric (e.g. all-digit account IDs) would
otherwise silently become an int64 column, breaking string-based joins and
lookups elsewhere in the pipeline.

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
a pipeline opportunity. Non-fatal timeline anomalies are reported as warnings,
as are near-duplicate opportunities - distinct `opportunity_id` values that
share the same account, product, engage date, and close value. This is a
warning rather than a failure because it can be a legitimate repeat sale
rather than a data-entry error; it exists so a manager can look, not so the
pipeline blocks on it.

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
