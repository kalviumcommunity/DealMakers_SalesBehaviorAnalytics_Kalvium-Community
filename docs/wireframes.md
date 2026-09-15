# Dashboard Wireframes

Text wireframes of the Streamlit dashboard layout, drawn before (and
cross-checked after) building `app.py`. These describe layout and
information hierarchy, not final copy or styling.

## Overall layout

```
+--------------------------------------------------------------------------+
| Sidebar               | Main content                                     |
|------------------------|--------------------------------------------------|
| Dataset                | Sales Behaviour Analytics          [title]       |
|  ( ) Demo Dataset       | dataset label | caption                          |
|  ( ) Uploaded Dataset   | [ How to read this dashboard - expander ]        |
|                         |                                                   |
| Filters                | [Opportunities][Closed][Won][Win Rate][Duration] |
|  Sales Agent  [multi]  | [Won Revenue]              <- KPI metric row     |
|  Deal Stage   [multi]  | [Download filtered opportunities (CSV)]          |
|  Product      [multi]  |                                                   |
|  Account      [multi]  | --- Alert Monitoring ---                         |
|  Engaged Between [date]| [Configure thresholds - expander]                |
|                         | (success/warning/error banners per breach)       |
|                         |                                                   |
|                         | --- Share This Report ---                        |
|                         | [Recipient email____] [Email this report]        |
+--------------------------------------------------------------------------+
```

## Below the fold (single scrolling page)

```
--- Sales Pipeline ---
[ bar chart: opportunities by deal stage ]
[ How is this calculated? (SQL) - expander ]

--- Pipeline Funnel and Drop-Off ---
[ funnel chart: Prospecting -> Engaging -> Won ]
[ table: stage | opportunities | drop-off % ]

--- Trends Over Time ---
[ line: opportunities engaged/month ] [ line: win rate/month + rolling avg ]
[ area: cumulative opportunities engaged ]

--- Distribution Analysis ---
[ histogram: deal duration ]           [ histogram: close value ]
skewness caption                        skewness + outlier count caption

--- Correlation Analysis ---
( ) Pearson  ( ) Spearman
[ heatmap: response_rate, response_time, activity, duration, value, stages ]

--- Behavioural Patterns by Deal Speed ---
[ table: Fast/Medium/Slow x response rate/time/activities ]
[ scatter: response time vs deal duration, coloured by speed ]

--- Won vs Lost Behaviour ---            --- Engagement-Level Comparison ---
[ table ]                                 [ table ]

--- Sales Agent Performance ---
[ table: top 15 agents ]  [Download agent summary (CSV)]
[ selectbox: inspect one agent ] -> [4 metric cards]

--- Deal Duration by Product ---
[ bar chart ]  [Download product summary (CSV)]

--- Opportunity Explorer ---
[ ] Compare two opportunities side by side
  unchecked: [ selectbox: one opportunity ] -> [ detail table ]
  checked:   [ selectbox: first ] [ selectbox: second ] -> [ side-by-side table ]

--- Coaching Signals ---
- bullet: response-rate difference, Fast vs Slow
- bullet: response-time difference
- bullet: activity-count difference
[ warning: behavioural data may be simulated ]
```

## Upload flow (Uploaded Dataset selected)

```
--- Upload New Data ---
[sales_pipeline.csv uploader (required)]
[email_history.csv uploader (optional)]
[crm_activities.csv uploader (optional)]
[stage_history.csv uploader (optional)]

if any files uploaded:
  [ tabs: one per uploaded file -> preview table + row/column caption ]

[Validate and process uploads] (disabled until sales_pipeline.csv present)

on success: green banner with row/column counts, "select Uploaded Dataset to view"
on failure: red banner with every validation error, newline-separated
```

## Design notes

- Filters, dataset selector, and alert thresholds live in the sidebar or a
  collapsed expander so the main column stays scannable top-to-bottom.
- Every chart section pairs with an optional "How is this calculated?"
  expander (`show_sql`) rather than a separate documentation page, so the
  explanation is next to the number it explains.
- The upload flow never lets a partially-valid file silently through:
  validation happens before any preview data reaches the feature pipeline.
