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

The application contains:

- **Overview:** pipeline stages, opportunity counts, closed and won deals, win rate, duration, and revenue.
- **Filters:** sales agent, deal stage, product, account, and an engagement date range.
- **Behaviour Analysis:** response rates, response times, activities, deal speed, and Won versus Lost comparisons.
- **Trends Over Time:** monthly opportunity volume and monthly win rate for closed deals.
- **Sales Agent Analysis:** descriptive comparisons of agent opportunities, activities, responses, and duration.
- **Opportunity Explorer:** a complete profile for one selected opportunity.
- **Data Upload:** validation, preview, and in-memory processing of compatible CSV files.
- **Coaching Signals:** descriptive differences between observed groups, without predictive recommendations.
- **CSV export:** download the filtered opportunities, agent summary, and product summary as CSV files.

Run the dashboard with:

```bash
.venv/bin/streamlit run app.py
```

## Uploading Data

Choose **Uploaded Dataset** in the sidebar. `sales_pipeline.csv` is required and must contain:

```text
opportunity_id, sales_agent, product, account, deal_stage,
engage_date, close_date, close_value
```

The following files are optional:

- `email_history.csv`
- `crm_activities.csv`
- `stage_history.csv`

The application validates CSV format, expected filenames, required columns, duplicates, dates, stages, numeric values, and behavioural opportunity IDs. It shows a preview before processing. Pipeline-only uploads work and are labelled `No history` where behavioural records are unavailable.

Uploaded data is processed in memory in the current Streamlit session. It does not overwrite the demo CSV files, feature dataset, or SQLite database. Switch back to **Demo Dataset** at any time to return to the original analysis.

## Project Structure

- `src/`: profiling, simulation, preparation, feature engineering, database loading, and upload processing.
- `data/raw/`: source CRM files and generated behavioural files.
- `data/processed/`: cleaned files, feature data, quality report, and local SQLite database.
- `sql/kpis.sql`: reusable KPI queries.
- `docs/`: pipeline, data quality, feature, database, source, and product documentation.
- `test_upload_processing.py`, `test_feature_engineering.py`: unit tests, run via `python -m unittest discover -p "test_*.py"`.
- `.github/workflows/tests.yml`: CI workflow that runs the test suite on every push and pull request to `main`.

## Testing

```bash
python -m unittest discover -p "test_*.py" -v
```

## Team

The team charter, roles, and working agreements are recorded in the project history and are maintained in this repository.
