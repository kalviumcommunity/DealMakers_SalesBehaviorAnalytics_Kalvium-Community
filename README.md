# DealMakers Sales Behavior Analytics

DealMakers is a descriptive Streamlit analytics product for B2B sales managers. It combines CRM opportunities with email history, CRM activities, and stage transitions to compare observed behaviour across the pipeline, deal outcomes, deal speed, agents, and individual opportunities.

This is not a machine-learning or prediction system. Behavioural data may be simulated for the prototype, so results must be described as associations and comparisons rather than causal conclusions.

## Pipeline

```text
CSV data -> preparation and validation -> opportunity features -> SQLite and SQL -> Streamlit dashboard
```

The demo dataset contains 8,800 opportunities. Run the existing preparation scripts when rebuilding the demo outputs:

```bash
.venv/bin/python src/profile_data.py
.venv/bin/python src/simulate_data.py
.venv/bin/python src/data_preparation.py
.venv/bin/python src/feature_engineering.py
.venv/bin/python src/load_database.py
```

## Dashboard

The dashboard is organised into sidebar-navigated sections (see
`DASHBOARD_PAGES` in `app.py`):

- **Overview:** pipeline stages, opportunity counts, closed and won deals, win rate, duration, and revenue; CSV export and a full report bundle (ZIP) download.
- **Pipeline, Funnel & Trends:** opportunities by stage, a cumulative Prospecting-to-Won funnel with drop-off percentages, monthly opportunity volume, and monthly win rate with a 3-month rolling average.
- **Distribution & Correlation:** deal-duration and close-value histograms with skewness and outlier counts, plus a Pearson/Spearman correlation heatmap.
- **Behavioural Analysis:** response rates, response times, activities, deal speed, Won versus Lost comparisons, engagement-level comparison, and Coaching Signals.
- **Agents & Products:** descriptive comparisons of agent opportunities, activities, responses, and duration; deal duration by product; CSV export for both summaries.
- **Opportunity Explorer:** a complete profile for one selected opportunity, or two side by side.
- **Alerts & Reporting:** configurable win-rate, response-rate, and response-time thresholds with severity-labelled warnings, and email delivery of an HTML KPI-and-alerts summary - see [docs/alerts-and-reporting.md](docs/alerts-and-reporting.md) for required SMTP environment variables.

Filters (sales agent, deal stage, product, account, engagement date range)
apply across every section and include a **Reset Filters** button. **Data
Upload** (CSV or JSON pipeline file) is available from the Dataset selector
regardless of section.

Run the dashboard with:

```bash
.venv/bin/streamlit run app.py
```

## Uploading Data

Choose **Uploaded Dataset** in the sidebar. `sales_pipeline.csv` (or
`sales_pipeline.json`, an array of the same records) is required and must
contain:

```text
opportunity_id, sales_agent, product, account, deal_stage,
engage_date, close_date, close_value
```

The following files are optional, and CSV-only:

- `email_history.csv`
- `crm_activities.csv`
- `stage_history.csv`

The application validates file format, expected filenames, required columns, duplicates, dates, stages, numeric values, and behavioural opportunity IDs. `deal_stage` values are normalised for case and whitespace (`won`, `WON `, `Won` all match) before validation. It shows a preview before processing. Pipeline-only uploads work and are labelled `No history` where behavioural records are unavailable.

Uploaded data is processed in memory in the current Streamlit session. It does not overwrite the demo CSV files, feature dataset, or SQLite database. Switch back to **Demo Dataset** at any time to return to the original analysis.

## Project Structure

- `src/`: profiling, simulation, preparation, feature engineering, database loading, and upload processing.
- `data/raw/`: source CRM files and generated behavioural files.
- `data/processed/`: cleaned files, feature data, quality report, and local SQLite database.
- `sql/kpis.sql`: reusable KPI queries, including JOIN and window-function (`RANK`, `LAG`) queries.
- `sql/views.sql`: `agent_team_performance` and `product_line_performance` views, joining `opportunity_features` to `sales_teams` and `products`.
- `docs/`: pipeline, data quality, feature, database, source, and product documentation.
- `test_upload_processing.py`, `test_feature_engineering.py`, `test_email_report.py`, `test_numeric_analysis.py`, `test_load_database.py`: unit tests, run via `python -m unittest discover -p "test_*.py"`.
- `.github/workflows/tests.yml`: CI workflow that runs the test suite on every push and pull request to `main`.

## Testing

```bash
python -m unittest discover -p "test_*.py" -v
```

## Team

The team charter, roles, and working agreements are recorded in the project history and are maintained in this repository.
