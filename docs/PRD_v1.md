# DealMakers Sales Behavior Analytics

## Problem

Sales coaching is often intuition-driven even when CRM opportunities, email
responses, activities, and stage transitions are available. Managers need a
clear descriptive view of behavioural differences associated with deal speed
and outcomes.

## Users and Goal

The primary user is a sales manager. DealMakers helps the manager understand
the pipeline, compare observed behaviours, review agents and opportunities, and
use compatible CRM exports without changing the demo dataset.

## Core Features

- Overview of pipeline stages, closed and won deals, win rate, duration, and revenue.
- Behaviour analysis across email response, response time, activities, stages, outcomes, and deal speed.
- Sales-agent comparison using descriptive metrics.
- Opportunity Explorer for sales, deal, email, activity, stage, and engagement details.
- Coaching Signals that describe observed group differences.
- Controlled upload of a required pipeline CSV and optional behavioural CSVs.

## Upload Workflow

The user selects Demo Dataset or Uploaded Dataset, uploads compatible CSV files,
previews them, validates them, and processes them in memory. A pipeline file is
required; email, activity, and stage-history files are optional. Missing
behavioural files produce safe `No history` features rather than an error.
Uploaded data never overwrites the demo source files or database.

## Analytics Approach

The pipeline standardizes and validates source data, aggregates event-level
records to one row per opportunity, loads the feature table into SQLite for the
demo workflow, and presents pandas/Plotly analytics in Streamlit. Results are
descriptive comparisons and associations only.

## Constraints and Validation

The product must not use machine learning, prediction, forecasting, lead
scoring, win probabilities, or causal claims. Upload validation checks CSV
format, filenames, required columns, empty files, duplicate identifiers,
required values, dates, deal stages, numeric values, and orphan behavioural
opportunity IDs. Errors must be understandable to a non-technical user.

## Success Criteria

- The existing demo dashboard, filters, SQL layer, and feature pipeline remain functional.
- Managers can inspect individual opportunities.
- Pipeline-only and full behavioural uploads both produce analytics.
- Invalid uploads are rejected without stack traces or permanent data changes.
- Documentation explains the product, pipeline, upload contract, and run command.

## Post-v1 Additions

Shipped after this PRD was written, within the same constraints (no ML,
predictions, or causal claims):

- An engagement date-range filter alongside the existing agent, stage,
  product, and account filters.
- A Trends Over Time view: monthly opportunity volume and monthly win rate
  for closed deals.
- CSV export for the filtered opportunities, agent summary, and product
  summary tables.
- Side-by-side comparison of two opportunities in the Opportunity Explorer.
- Inline "How is this calculated?" SQL, sourced directly from `sql/kpis.sql`,
  next to each descriptive comparison on the dashboard.
- A CI workflow that runs the test suite on every push and pull request to `main`.
