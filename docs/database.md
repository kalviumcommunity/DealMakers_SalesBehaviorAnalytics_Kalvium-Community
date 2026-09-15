# SQLite Analytical Layer

`src/load_database.py` builds `data/processed/sales_analytics.db` from the
versioned opportunity feature CSV. It recreates the database on every run, so
the dashboard and SQL queries use the same feature schema.

The database contains four tables and two views:

- `opportunity_features` - one row per opportunity (the main analytical table).
- `sales_teams` - agent, manager, and regional office, loaded from `data/raw/sales_teams.csv`.
- `products` - product, series, and list price, loaded from `data/raw/products.csv`.
- `pipeline_metadata` - a row-count loading check for each table above.
- `agent_team_performance` (view) - `opportunity_features` JOINed to `sales_teams`, aggregated by regional office, manager, and agent.
- `product_line_performance` (view) - `opportunity_features` LEFT JOINed to `products`, aggregated by product. LEFT, not INNER: `opportunity_features.product` includes `"GTXPro"`, which does not match `"GTX Pro"` in `products` - an INNER JOIN would silently drop those rows.

Indexes support filtering by opportunity ID, deal stage, sales agent, product,
and the join keys on `sales_teams`/`products`. The two views are (re)created
from `sql/views.sql` every time the database is built, so they always match
the current data - see that file's `DROP VIEW IF EXISTS` + `CREATE VIEW`
pairs. `sql/kpis.sql` also has window-function queries (`RANK`, `LAG`) built
on top of `agent_team_performance`.

```bash
.venv/bin/python src/feature_engineering.py
.venv/bin/python src/load_database.py
```

The SQLite file is generated locally and excluded from Git; recreate it from
the committed feature dataset whenever the pipeline changes.

## Deployed environments (e.g. Streamlit Community Cloud)

A fresh deploy clones the repo, so it has `data/processed/opportunity_features.csv`
(committed) but not `sales_analytics.db` (gitignored). `app.py`'s
`load_demo_data()` detects this and calls `build_database()` automatically on
first load, using the committed CSV and the committed `data/raw/sales_teams.csv`
/ `products.csv`. This keeps the generated `.db` file out of Git while still
working out of the box after a deploy - no manual setup step required on the
hosting platform.
