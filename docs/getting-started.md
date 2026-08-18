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
pip install pandas
```

The project currently uses the following Python packages:

| Package | Purpose |
|---------|---------|
| `pandas` | Data loading, manipulation, and exploratory analysis |

As the project grows, a `requirements.txt` will be added. You can then install everything at once with:

```bash
pip install -r requirements.txt
```

---

## 4. Prepare the Dataset

The raw data files are already included in the repository under `data/raw/`. Verify they are present:

```
data/
└── raw/
    ├── sales_pipeline.csv    ← Main analysis dataset (8,800 sales opportunities)
    ├── accounts.csv          ← Company/account information
    ├── products.csv          ← Product catalogue
    ├── sales_teams.csv       ← Sales agent and team info
    └── data_dictionary.csv   ← Field definitions
```

> **Source:** CRM Sales Opportunities — Public dataset from [Kaggle](https://www.kaggle.com/).
> See [`docs/dataset-source.md`](./dataset-source.md) for full details.

---

## 5. Run the Analysis Script

Make sure you run the script **from the root of the repository** so that the relative data paths resolve correctly:

```bash
# From the project root directory
python src/profile_data.py
```

### Expected Output

Running the script will print the following to your terminal:

- Dataset shape (rows × columns)
- Column names
- First 5 rows preview
- Data types for each column
- Missing value counts per column
- Distribution of deal stages
- Full data dictionary
- Missing `close_date` breakdown by deal stage
- Missing `close_value` breakdown by deal stage
- Missing `engage_date` breakdown by deal stage
- Count of closed deals (Won / Lost)
- Win rate among closed deals (%)
- Deal duration statistics (days from engage to close)
- Close value statistics
- Top 10 sales agents by deal count
- Product distribution

---

## 6. Deactivate the Virtual Environment

When you are done working, deactivate the virtual environment:

```bash
deactivate
```

---

## Project Structure

```
DealMakers_SalesBehaviorAnalytics_Kalvium-Community/
│
├── data/
│   └── raw/                    # Raw CSV datasets
│       ├── sales_pipeline.csv
│       ├── accounts.csv
│       ├── products.csv
│       ├── sales_teams.csv
│       └── data_dictionary.csv
│
├── docs/                       # Project documentation
│   ├── getting-started.md      ← You are here
│   ├── dataset-source.md       # Dataset origin and field descriptions
│   └── project-overview.md     # Project context and goals
│
├── src/                        # Python source code
│   └── profile_data.py         # Data profiling and EDA script
│
├── .gitignore
└── README.md
```

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'pandas'`
You forgot to install dependencies or your virtual environment is not active.
```bash
# Activate the venv first, then:
pip install pandas
```

### `FileNotFoundError: data/raw/sales_pipeline.csv`
You are not running the script from the **project root**. Always `cd` into the repo root before running `python src/profile_data.py`.

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
