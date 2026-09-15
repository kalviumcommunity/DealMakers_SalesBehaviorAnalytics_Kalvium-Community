# Opportunity-Level Feature Engineering

`src/feature_engineering.py` creates `data/processed/opportunity_features.csv`.
Each row represents one CRM opportunity, retaining pipeline fields alongside
descriptive behavioural aggregates. There is no predictive model.

## Pipeline fields

- `is_closed`, `is_won`, and `deal_duration_days` make outcome KPIs consistent.
- `deal_speed` divides closed-deal duration into Fast, Medium, and Slow thirds;
  open opportunities are labelled `Open`. Tier assignment uses `numpy.select`
  over vectorised boolean conditions rather than sequential `.loc` writes.
- `is_close_value_outlier` flags won deals whose `close_value` falls outside
  the IQR fences (1.5x interquartile range) of all won deals, using
  `src/numeric_analysis.py`'s NumPy-vectorised `iqr_outliers`. It is
  descriptive only - flagged deals are not removed or treated differently
  anywhere else in the pipeline.

## Behavioural fields

- Email: sent/responded counts, response rate, average and median response time.
- Activity: total, successful, unique-type, call, meeting, demo, and follow-up counts.
- Stage: transition count, total stage days, and average stage days.
- Engagement: `has_behavioural_history` and a transparent Low/Medium/High
  `engagement_level` based on email response rate and activity volume.

Prospecting opportunities without behavioural records are explicitly labelled
`No history`; null response times remain null when a customer did not respond.

## Run

```bash
.venv/bin/python src/data_preparation.py
.venv/bin/python src/feature_engineering.py
```

This CSV is the single source for the SQLite analytical layer and dashboard.
