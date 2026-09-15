# Root Cause Investigation Workflow

A structured way to use the dashboard's existing filters and comparisons to
investigate a metric problem, instead of jumping straight to a conclusion.
This is a workflow over existing features - it does not require or
introduce any new dashboard component.

## The workflow

1. **Confirm the signal is real, not a filter artifact.** Check Alert
   Monitoring first. If a threshold is breached, note whether it's breached
   for the whole Demo Dataset or only for your current sidebar filter
   selection - clear all filters and re-check before investigating further.

2. **Narrow by time.** Use the "Engaged Between" sidebar filter to isolate
   the period where the metric looks worst, then check Trends Over Time's
   monthly win-rate chart (with its 3-month rolling average) to see whether
   the problem is a one-month blip or a sustained shift. A blip that
   disappears in the rolling average is lower priority than a sustained
   drop.

3. **Narrow by segment.** With the time window fixed, add one filter at a
   time - Sales Agent, then Product, then Account - and watch the KPI row
   update. If the metric only looks bad for one agent or one product, that's
   the segment to focus on, not the whole pipeline.

4. **Compare, don't assume.** Once you have a suspect segment, use:
   - **Sales Agent Performance** to compare that agent against the
     dashboard-wide averages already shown in the table.
   - **Opportunity Explorer's** side-by-side comparison to inspect two
     specific opportunities from that segment - one that fits the pattern,
     one that doesn't - and look for what actually differs between them
     (response rate, activity count, stage transitions), rather than
     guessing.
   - **Correlation Analysis** to check whether the metric you're
     investigating moves with any other numeric field in this segment, as a
     starting hypothesis, not a conclusion.

5. **Check the SQL, not just the chart.** Every comparison section has a
   "How is this calculated? (SQL)" expander. Before concluding a number is
   wrong, confirm you're reading the same aggregation the chart is - e.g.
   whether a rate is computed over all opportunities or only closed ones.

6. **Write down the association, not the cause.** Per this project's
   constraints (see `docs/PRD_v1.md`), the output of this workflow is a
   documented association ("agent X's opportunities show half the response
   rate of the team average in Q2") for a manager to follow up on directly,
   not an automated explanation of why it happened.

## Worked example

Suppose Alert Monitoring flags win rate below the 40% threshold:

1. Clear filters - the alert clears too, so it's specific to a prior
   selection, not dataset-wide.
2. Re-apply just the date range that had been selected - the alert
   reappears, confirming it's time-bound, not a single filter combination
   coincidence.
3. Add Sales Agent filters one at a time - the alert only reappears for two
   of five agents.
4. For those two agents, Sales Agent Performance shows response rate well
   below the team average; Opportunity Explorer comparison shows their lost
   deals have near-zero CRM activity count compared to their won deals.
5. Correlation Analysis (filtered to those two agents) shows activity_count
   correlates with is_won more strongly than it does dataset-wide.
6. Documented finding: "For agents A and B in [date range], lost
   opportunities show markedly lower CRM activity counts than won ones -
   worth a coaching conversation about activity cadence for this pair,"
   not "low activity causes losses."
