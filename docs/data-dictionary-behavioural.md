# Data Dictionary - Behavioural and Engineered Fields

`docs/dataset-source.md` documents the original Kaggle fields. This covers
the fields that don't exist in that source: the simulated behavioural data
(`src/simulate_data.py`) and the engineered features built on top of it
(`src/feature_engineering.py`). It exists because these fields have
non-obvious meaning, thresholds, or null semantics that aren't visible from
the column name alone.

## Simulated behavioural data

| Field | File | Description | Ambiguity notes |
|---|---|---|---|
| `response_status` | `email_history.csv` | `Responded` or `No Response` | Drives `response_rate`; not a measure of email quality or content. |
| `response_time_hours` | `email_history.csv` | Hours between `sent_at` and `responded_at` | Null when `response_status` is `No Response` - a null here is not a fast response, it's a non-response. |
| `activity_outcome` | `crm_activities.csv` | Free-text outcome (`Connected`, `No answer`, `Completed`, ...) | Only `Connected`, `Completed`, `Interested`, `Responded` count as `successful_activity` in feature engineering; other completed-sounding outcomes (`Rescheduled`) do not. |
| `days_in_previous_stage` | `stage_history.csv` | Days spent in `from_stage` before this transition | Summed per opportunity into `total_stage_days`; a large value can mean either genuine stalling or a data gap between simulated transitions. |

## Engineered KPI fields (`opportunity_features`)

| Field | Description | Ambiguity / threshold notes |
|---|---|---|
| `response_rate` | Responded emails / total emails for the opportunity | Null (not zero) when `email_count` is 0 - an opportunity with no emails has no measurable response rate, which is different from a 0% response rate. |
| `engagement_level` | `High` / `Medium` / `Low` / `No history` | Thresholds are **relative to the current dataset**: `High` requires response rate >= 60% AND activity count >= that dataset's median activity count among engaged opportunities. Re-running on a different dataset changes the median, and therefore changes who qualifies as `High` - this is not a fixed, portable threshold. |
| `deal_speed` | `Fast` / `Medium` / `Slow` / `Open` | Fast/Medium/Slow are the closed-deal duration tercile boundaries **of the current filtered selection**, not fixed day counts. The same 20-day deal can be `Fast` in one filter and `Medium` in another. |
| `is_close_value_outlier` | IQR-based outlier flag on `close_value` for won deals | Computed against **all won deals in the dataset**, not per-product or per-agent - a legitimately high-value enterprise deal in an otherwise low-value product line will be flagged, since the fence is dataset-wide. |
| `has_behavioural_history` | 1 if `email_count` > 0, else 0 | An opportunity can have CRM activities or stage transitions but still show `has_behavioural_history = 0` if it has zero emails - this field is email-specific, not "any behavioural data exists". |
| `engage_day_of_week`, `engage_month_name`, `engage_week_of_year` | Calendar features from `engage_date` | Null (not a default like "Monday" or week 0) when `engage_date` itself is null, which happens for open Prospecting opportunities. |

## Where thresholds live

Alert thresholds (win rate, response rate, response time - see
[docs/alerts-and-reporting.md](./alerts-and-reporting.md)) are configured per
dashboard session and are **not** the same numbers as the `engagement_level`
or `deal_speed` thresholds above, which are computed from the data itself.
Don't assume changing one changes the other.
