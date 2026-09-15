import sqlite3
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.load_database import build_database


def _features():
    return pd.DataFrame({
        "opportunity_id": ["A1", "A2"],
        "sales_agent": ["Agent One", "Agent Two"],
        "product": ["Widget", "Widget"],
        "deal_stage": ["Won", "Lost"],
        "is_closed": [1, 1],
        "is_won": [1, 0],
        "deal_duration_days": [5, 10],
        "response_rate": [0.5, 0.2],
        "activity_count": [3, 1],
        "engagement_level": ["High", "Low"],
        "close_value": [1000, None],
    })


class BuildDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        tmp_path = Path(self.tmp.name)
        self.raw_data = tmp_path / "raw"
        self.raw_data.mkdir()
        pd.DataFrame({
            "sales_agent": ["Agent One", "Agent Two"],
            "manager": ["Manager A", "Manager A"],
            "regional_office": ["Central", "Central"],
        }).to_csv(self.raw_data / "sales_teams.csv", index=False)
        pd.DataFrame({
            "product": ["Widget"], "series": ["Basic"], "sales_price": [100],
        }).to_csv(self.raw_data / "products.csv", index=False)

        self.views_path = tmp_path / "views.sql"
        self.views_path.write_text(
            "DROP VIEW IF EXISTS agent_summary;\n"
            "CREATE VIEW agent_summary AS "
            "SELECT sales_agent, COUNT(*) AS opportunities FROM opportunity_features GROUP BY sales_agent;"
        )
        self.db_path = tmp_path / "test.db"

    def tearDown(self):
        self.tmp.cleanup()

    def test_reference_tables_and_view_are_created(self):
        build_database(_features(), db_path=self.db_path, raw_data=self.raw_data, views_path=self.views_path)
        with sqlite3.connect(self.db_path) as connection:
            names = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')")}
        self.assertIn("sales_teams", names)
        self.assertIn("products", names)
        self.assertIn("agent_summary", names)

    def test_view_can_be_queried(self):
        build_database(_features(), db_path=self.db_path, raw_data=self.raw_data, views_path=self.views_path)
        with sqlite3.connect(self.db_path) as connection:
            rows = connection.execute("SELECT * FROM agent_summary ORDER BY sales_agent").fetchall()
        self.assertEqual(rows, [("Agent One", 1), ("Agent Two", 1)])

    def test_join_between_opportunity_features_and_sales_teams(self):
        build_database(_features(), db_path=self.db_path, raw_data=self.raw_data, views_path=self.views_path)
        with sqlite3.connect(self.db_path) as connection:
            rows = connection.execute(
                "SELECT o.opportunity_id, st.regional_office "
                "FROM opportunity_features o JOIN sales_teams st ON st.sales_agent = o.sales_agent "
                "ORDER BY o.opportunity_id"
            ).fetchall()
        self.assertEqual(rows, [("A1", "Central"), ("A2", "Central")])

    def test_missing_views_file_is_tolerated(self):
        build_database(_features(), db_path=self.db_path, raw_data=self.raw_data, views_path=Path(self.tmp.name) / "missing.sql")
        with sqlite3.connect(self.db_path) as connection:
            names = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn("opportunity_features", names)


if __name__ == "__main__":
    unittest.main()
