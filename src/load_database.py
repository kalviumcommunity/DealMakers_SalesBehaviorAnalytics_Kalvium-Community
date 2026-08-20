"""Create a query-ready SQLite database from the opportunity feature dataset."""

import sqlite3
from pathlib import Path

import pandas as pd


CSV_PATH = Path("data/processed/opportunity_features.csv")
DB_PATH = Path("data/processed/sales_analytics.db")
TABLE_NAME = "opportunity_features"
REQUIRED_COLUMNS = {
    "opportunity_id", "sales_agent", "product", "deal_stage", "is_closed", "is_won",
    "deal_duration_days", "response_rate", "activity_count", "engagement_level",
}


def load_features(csv_path: Path = CSV_PATH) -> pd.DataFrame:
    features = pd.read_csv(csv_path)
    missing = REQUIRED_COLUMNS - set(features.columns)
    if missing:
        raise ValueError(f"Feature dataset is missing columns: {', '.join(sorted(missing))}")
    if features["opportunity_id"].duplicated().any():
        raise ValueError("Feature dataset must contain one row per opportunity.")
    return features


def build_database(features: pd.DataFrame, db_path: Path = DB_PATH) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as connection:
        features.to_sql(TABLE_NAME, connection, if_exists="replace", index=False)
        connection.execute("CREATE UNIQUE INDEX idx_opportunity_id ON opportunity_features(opportunity_id)")
        connection.execute("CREATE INDEX idx_deal_stage ON opportunity_features(deal_stage)")
        connection.execute("CREATE INDEX idx_sales_agent ON opportunity_features(sales_agent)")
        connection.execute("CREATE INDEX idx_product ON opportunity_features(product)")
        connection.execute("DROP TABLE IF EXISTS pipeline_metadata")
        connection.execute("CREATE TABLE pipeline_metadata (dataset_name TEXT PRIMARY KEY, row_count INTEGER NOT NULL)")
        connection.execute("INSERT INTO pipeline_metadata VALUES (?, ?)", (TABLE_NAME, len(features)))


def main() -> None:
    features = load_features()
    build_database(features)
    with sqlite3.connect(DB_PATH) as connection:
        rows = connection.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]
    print(f"Database created: {DB_PATH}")
    print(f"Rows loaded: {rows}")


if __name__ == "__main__":
    main()
