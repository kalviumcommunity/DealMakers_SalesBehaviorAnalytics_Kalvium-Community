# Executive Summary (Example) - Demo Dataset

This is a worked example of the stakeholder-facing summary a sales manager
could produce from the Demo Dataset view of the dashboard, generated
2026-09-15. It is a template to copy and re-run numbers against, not a
saved historical report - the dashboard's "Share This Report" feature sends
a shorter KPI-and-alerts email; this document is the longer narrative form
for a leadership review, per `docs/data-quality.md`'s constraint that
findings stay descriptive, not causal.

## Context

8,800 opportunities across 35 agents and 7 products, spanning October 2016
to December 2017. 6,711 are closed (Won or Lost); the rest remain in
Prospecting or Engaging.

## Headline numbers

- **Win rate:** 63.2% of closed deals were won, for $10.0M in won revenue.
- **Median deal duration:** 45 days from engagement to close.
- **Average response rate:** 49.2% of emails receive a customer response;
  average response time is 32.6 hours.
- **Funnel:** of all 8,800 opportunities, 94.3% reach Engaging or beyond;
  of those, 51.1% go on to Win. The largest drop-off is between Engaging and
  Won, not between Prospecting and Engaging.

## Findings

**Fast deals are not more responsive deals.** The intuitive assumption is
that highly responsive customers close faster. In this dataset it's the
opposite: opportunities in the `Fast` speed tier have a 33.7% average email
response rate, versus 57.1% for `Slow` deals - roughly 23 points lower, not
higher. Read as an association, not a cause: a short deal cycle gives fewer
calendar days for email exchanges to happen at all, so a low response-rate
number on a fast deal may simply reflect less elapsed time, not a
disengaged customer.

**Agent win rates span a real range.** The top three agents by win rate
(Reed Clapper 65.4%, Garret Kinder 61.0%, Donn Cantrell 57.5%) outperform
the bottom three (Gladys Colclough 42.6%, Markita Hansen 42.5%, Lajuana
Vencill 40.8%) by roughly 20 percentage points on comparable opportunity
volume (237-317 opportunities each). This is a large enough gap, on similar
sample sizes, to be worth a coaching conversation - the dashboard's Sales
Agent Performance and Opportunity Explorer sections support that
conversation without asserting why the gap exists.

**Response time exceeds the default alert threshold.** The dataset-wide
average response time (32.6 hours) breaches the dashboard's default
24-hour alert threshold. See Alert Monitoring for the current, adjustable
threshold configuration.

**15 won deals are statistical outliers on value.** Flagged by the
IQR-based `is_close_value_outlier` field - see
`docs/data-dictionary-behavioural.md` for why this is dataset-wide, not
per-product, and can flag legitimate large deals rather than errors.

## Risks and caveats

- Behavioural data (email, activity, and stage-transition history) is
  **simulated** for this prototype, not observed. Treat every finding above
  as an association worth investigating, not a proven cause.
- `engagement_level` and `deal_speed` thresholds are computed relative to
  this dataset and will shift if the underlying data changes - see the data
  dictionary before comparing them across two different report runs.
- 64 near-duplicate opportunities were flagged during data preparation
  (same account, product, engage date, and close value). These were not
  removed; if they are data-entry duplicates rather than repeat sales, the
  win-rate and revenue figures above are very slightly inflated.

## Recommended next steps

1. Review the bottom three agents' Opportunity Explorer profiles alongside
   the top three, to see whether the gap tracks a specific product, account
   segment, or activity pattern rather than agent skill alone.
2. Investigate the Engaging-to-Won drop-off specifically, since it accounts
   for more lost opportunities than the Prospecting-to-Engaging step.
3. Re-run data preparation's near-duplicate check after resolving the 64
   flagged rows, to confirm whether the win-rate and revenue figures above
   change materially.
