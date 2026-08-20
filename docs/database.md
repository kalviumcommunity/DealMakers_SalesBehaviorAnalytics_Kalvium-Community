# SQLite Analytical Layer

`src/load_database.py` builds `data/processed/sales_analytics.db` from the
versioned opportunity feature CSV. It recreates the database on every run, so
the dashboard and SQL queries use the same feature schema.

The database contains `opportunity_features` (one row per opportunity) and
`pipeline_metadata` (a row-count loading check). Indexes support filtering by
opportunity ID, deal stage, sales agent, and product.

```bash
.venv/bin/python src/feature_engineering.py
.venv/bin/python src/load_database.py
```

The SQLite file is generated locally and excluded from Git; recreate it from
the committed feature dataset whenever the pipeline changes.
