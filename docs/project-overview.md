# Project Overview — DealMakers Sales Behavior Analytics

## What Is This Project?

**DealMakers Sales Behavior Analytics** is a data analytics project that explores and analyses real-world CRM (Customer Relationship Management) sales data to uncover insights about sales behavior, deal outcomes, and agent performance.

The project is built by **Team DealMakers** as part of the Kalvium Community's Analytics sprint.

---

## Problem Statement

Sales teams generate large volumes of data about deals — when they were engaged, which products were pitched, which agent handled them, and whether they were ultimately won or lost. However, raw CRM data alone does not reveal *why* deals succeed or fail.

This project aims to:

1. **Profile and understand** the structure and quality of real CRM sales opportunity data.
2. **Identify patterns** in deal stages, durations, agent performance, and product success rates.
3. **Lay the groundwork** for simulating synthetic behavioral data (e.g., email response history, CRM activity logs) that is not present in the raw dataset but is critical for deeper behavioral analysis.

---

## Goals

| Phase | Goal |
|-------|------|
| **Phase 1 — Data Profiling** | Understand dataset shape, data types, missing values, and distributions |
| **Phase 2 — Exploratory Analysis** | Identify win rates, deal durations, top agents, and product trends |
| **Phase 3 — Behavioral Simulation** | Generate synthetic behavioral records linked to real `opportunity_id` values |
| **Phase 4 — Insights & Reporting** | Produce actionable findings from the combined real + synthetic data |

---

## Dataset

The project uses the **CRM Sales Opportunities** dataset from Kaggle — a publicly available dataset containing 8,800 sales opportunities across multiple products, agents, and accounts.

### Key Fields

| Field | Description |
|-------|-------------|
| `opportunity_id` | Unique identifier for each sales deal |
| `sales_agent` | The sales agent responsible for the deal |
| `product` | The product being sold |
| `account` | The company/client being targeted |
| `deal_stage` | Current stage: `Prospecting`, `Engaging`, `Won`, `Lost` |
| `engage_date` | Date the deal entered the engagement phase |
| `close_date` | Date the deal was closed (Won or Lost) |
| `close_value` | Revenue value of the closed deal (USD) |

> For the full data dictionary, see [`docs/dataset-source.md`](./dataset-source.md).

---

## Current Analysis (`src/profile_data.py`)

The current script performs **Phase 1 & 2** work — exploratory data analysis (EDA):

- Loads `data/raw/sales_pipeline.csv` and `data/raw/data_dictionary.csv`
- Reports missing values and whether they correlate with open (non-closed) deals
- Computes:
  - **Win rate** among closed deals
  - **Deal duration** (days from `engage_date` to `close_date`)
  - **Close value** statistics (min, max, median, mean)
  - **Top 10 sales agents** by deal volume
  - **Product distribution** across all deals

---

## Why Synthetic Behavioral Data?

The Kaggle CRM dataset captures *outcomes* (Won/Lost) but lacks *process* data:

- How many emails were exchanged before closing?
- How quickly did agents respond to client queries?
- What CRM activities (calls, demos, follow-ups) preceded a win vs. a loss?

Since this behavioral data is unavailable publicly, the team plans to **simulate it** in a realistic way using the distributions observed in the real data (e.g., deal durations, win rates by product). All simulated data will be clearly labeled as synthetic and tied back to real `opportunity_id` values.

---

## Tech Stack

| Technology | Role |
|------------|------|
| **Python 3.9+** | Core language |
| **pandas** | Data manipulation and EDA |
| **Kaggle CRM Dataset** | Real-world data source |

---

## Team

| Member | Role | Strength |
|--------|------|----------|
| **Navaneeth M** | Project Admin | Git/GitHub, programming fundamentals |
| **Nishat Ayub** | Team Member | Problem-solving, dev tooling |
| **Monish GR** | Team Member | Python, logical thinking |

### Working Agreements
- PR review turnaround: **same day**
- Blockers: try solo for **30 minutes**, then escalate
- Standup format: **Yesterday / Today / Blockers**
- Primary channel: **Google Message**

---

## Documentation Index

| Document | Description |
|----------|-------------|
| [`docs/getting-started.md`](./getting-started.md) | How to install, set up, and run the project locally |
| [`docs/dataset-source.md`](./dataset-source.md) | Dataset origin, files, and field descriptions |
| [`docs/project-overview.md`](./project-overview.md) | Project context, goals, and tech stack (this file) |
| [`README.md`](../README.md) | Team charter and working agreements |
