# Getting Started — DealMakers Sales Behavior Analytics

This guide explains how to set up and run the project locally on your machine.

---

## Prerequisites

Before you begin, make sure the following are installed on your system:

| Tool | Minimum Version | How to check |
|------|----------------|--------------|
| Python | 3.9+ | `python --version` |
| pip | Latest | `pip --version` |
| Git | Any recent | `git --version` |

> **Tip:** It is strongly recommended to use a Python virtual environment to keep dependencies isolated.

---

## 1. Clone the Repository

```bash
git clone https://github.com/kalviumcommunity/DealMakers_SalesBehaviorAnalytics_Kalvium-Community.git
cd DealMakers_SalesBehaviorAnalytics_Kalvium-Community
```

---

## 2. Create a Virtual Environment

### On macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### On Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### On Windows (Command Prompt)
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

> **Note:** You should see `(.venv)` appear at the start of your terminal prompt once the virtual environment is active.

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs pandas, Streamlit, Plotly, and everything else the pipeline and dashboard need.

---

## 4. Rebuild the Demo Dataset

The raw source files are already included under `data/raw/`, but the generated
demo outputs (simulated behavioural data, cleaned files, feature dataset, and
SQLite database) are not committed to the repository. Build them by running
the pipeline scripts in order from the project root:

```bash
.venv/bin/python src/profile_data.py
.venv/bin/python src/simulate_data.py
.venv/bin/python src/data_preparation.py
.venv/bin/python src/feature_engineering.py
.venv/bin/python src/load_database.py
```

| Step | Script | Produces |
|------|--------|----------|
| Profile | `src/profile_data.py` | Console EDA summary of the raw pipeline data |
| Simulate | `src/simulate_data.py` | `data/raw/email_history.csv`, `crm_activities.csv`, `stage_history.csv` |
| Prepare | `src/data_preparation.py` | `data/processed/cleaned/`, `data/processed/data_quality_report.json` |
| Engineer features | `src/feature_engineering.py` | `data/processed/opportunity_features.csv` |
| Load database | `src/load_database.py` | `data/processed/sales_analytics.db` |

See [`docs/PIPELINE_DESIGN.md`](./PIPELINE_DESIGN.md) for the full pipeline diagram and
[`docs/feature-engineering.md`](./feature-engineering.md) / [`docs/data-quality.md`](./data-quality.md)
for what each stage does.

---

## 5. Run the Dashboard

```bash
.venv/bin/streamlit run app.py
```

This opens the Streamlit dashboard in your browser (defaults to
`http://localhost:8501`). The dashboard reads from
`data/processed/sales_analytics.db`, so step 4 must complete first.

The dashboard includes an Overview, Behaviour Analysis, Trends Over Time,
Sales Agent Analysis, Opportunity Explorer, Data Upload, and Coaching Signals.
See the [README](../README.md) for a full feature list and the upload contract.

---

## 6. Run the Tests

```bash
python -m unittest discover -p "test_*.py" -v
```

This runs the full test suite (upload validation and feature-engineering
tests). The same command runs automatically in CI on every push and pull
request against `main` — see `.github/workflows/tests.yml`.

---

## 7. Deactivate the Virtual Environment

When you are done working, deactivate the virtual environment:

```bash
deactivate
```

---

## Project Structure

```
DealMakers_SalesBehaviorAnalytics_Kalvium-Community/
│
├── .github/workflows/          # CI: runs the test suite on push/PR
├── data/
│   ├── raw/                    # Source CRM files + generated behavioural files
│   └── processed/              # Cleaned files, feature dataset, SQLite database
├── docs/                       # Project documentation
│   ├── getting-started.md      ← You are here
│   ├── dataset-source.md       # Dataset origin and field descriptions
│   ├── project-overview.md     # Project context and goals
│   ├── PIPELINE_DESIGN.md      # End-to-end pipeline diagram
│   ├── behavioural-data-design.md  # Design of the simulated behavioural data
│   ├── data-quality.md         # Validation rules and quality checks
│   ├── feature-engineering.md  # Opportunity feature definitions
│   ├── database.md             # SQLite analytical layer
│   └── PRD_v1.md               # Product requirements
├── sql/kpis.sql                 # Reusable KPI queries against opportunity_features
├── src/                         # Profiling, simulation, preparation, feature
│   │                             engineering, database loading, upload processing
├── app.py                       # Streamlit dashboard
├── test_upload_processing.py    # Upload validation tests
├── test_feature_engineering.py  # Feature engineering tests
├── requirements.txt
└── README.md
```

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'streamlit'` (or `pandas`, `plotly`, etc.)
Your virtual environment is not active, or dependencies were not installed.
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### `Analytics database not found. Run src/load_database.py first.`
You skipped step 4. Run the five pipeline scripts in order from the project root.

### `FileNotFoundError: data/raw/sales_pipeline.csv`
You are not running the script from the **project root**. Always `cd` into the
repo root before running any `src/*.py` script.

### `python: command not found` (Linux/macOS)
Try `python3` instead:
```bash
python3 src/profile_data.py
```

---

## Team

| Member | Role |
|--------|------|
| Navaneeth M | Project Admin |
| Nishat Ayub | Team Member |
| Monish GR | Team Member |

See `README.md` for team agreements and commitments.
