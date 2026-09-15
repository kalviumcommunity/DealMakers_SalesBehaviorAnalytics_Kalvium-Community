"""Cross-check that SQL aggregates and pandas aggregates agree on the same data.

This is not a test of business logic (that's covered by test_feature_engineering.py)
- it exists purely to catch the case where a SQL query in sql/kpis.sql and the
equivalent pandas computation in app.py silently drift apart (e.g. one is
updated and the other isn't).
"""

import sqlite3
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.load_database import build_database

TOLERANCE = 0.01


def _sample_features(n=500):
    import random

    random.seed(42)
    stages = ["Won"] * 200 + ["Lost"] * 150 + ["Engaging"] * 100 + ["Prospecting"] * 50
    rows = []
    for i in range(n):
        stage = stages[i % len(stages)]
        is_closed = int(stage in ("Won", "Lost"))
        is_won = int(stage == "Won")
        rows.append({
            "opportunity_id": f"OPP{i}",
            "sales_agent": f"Agent {i % 5}",
            "product": "Product",
            "deal_stage": stage,
            "is_closed": is_closed,
            "is_won": is_won,
            "deal_duration_days": random.randint(1, 90) if is_closed else None,
            "response_rate": round(random.uniform(0.1, 0.9), 2),
            "activity_count": random.randint(0, 20),
            "engagement_level": random.choice(["Low", "Medium", "High"]),
            "close_value": round(random.uniform(100, 5000), 2) if is_won else None,
        })
    return pd.DataFrame(rows)


class SqlPythonParityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        tmp_path = Path(self.tmp.name)
        self.raw_data = tmp_path / "raw"
        self.raw_data.mkdir()
        pd.DataFrame({"sales_agent": [], "manager": [], "regional_office": []}).to_csv(self.raw_data / "sales_teams.csv", index=False)
        pd.DataFrame({"product": [], "series": [], "sales_price": []}).to_csv(self.raw_data / "products.csv", index=False)
        self.db_path = tmp_path / "test.db"
        self.features = _sample_features()
        build_database(self.features, db_path=self.db_path, raw_data=self.raw_data, views_path=tmp_path / "missing.sql")
        self.connection = sqlite3.connect(self.db_path)

    def tearDown(self):
        self.connection.close()
        self.tmp.cleanup()

    def test_overall_win_rate_matches(self):
        sql_value = self.connection.execute(
            "SELECT 100.0 * SUM(is_won) / SUM(is_closed) FROM opportunity_features"
        ).fetchone()[0]
        closed = self.features[self.features["is_closed"] == 1]
        python_value = len(closed[closed["is_won"] == 1]) / len(closed) * 100
        self.assertAlmostEqual(sql_value, python_value, delta=TOLERANCE)

    def test_average_deal_duration_matches(self):
        sql_value = self.connection.execute(
            "SELECT AVG(deal_duration_days) FROM opportunity_features WHERE is_closed = 1"
        ).fetchone()[0]
        python_value = self.features.loc[self.features["is_closed"] == 1, "deal_duration_days"].mean()
        self.assertAlmostEqual(sql_value, python_value, delta=TOLERANCE)

    def test_win_rate_by_agent_matches(self):
        sql_rows = self.connection.execute(
            "SELECT sales_agent, 100.0 * SUM(is_won) / NULLIF(SUM(is_closed), 0) "
            "FROM opportunity_features GROUP BY sales_agent ORDER BY sales_agent"
        ).fetchall()
        sql_by_agent = dict(sql_rows)

        closed = self.features[self.features["is_closed"] == 1]
        python_by_agent = (closed.groupby("sales_agent")["is_won"].mean() * 100).to_dict()

        self.assertEqual(set(sql_by_agent), set(python_by_agent))
        for agent, sql_value in sql_by_agent.items():
            self.assertAlmostEqual(sql_value, python_by_agent[agent], delta=TOLERANCE, msg=f"mismatch for {agent}")

    def test_average_response_rate_matches(self):
        sql_value = self.connection.execute("SELECT AVG(response_rate) FROM opportunity_features").fetchone()[0]
        python_value = self.features["response_rate"].mean()
        self.assertAlmostEqual(sql_value, python_value, delta=TOLERANCE)

    def test_row_count_matches(self):
        sql_count = self.connection.execute("SELECT COUNT(*) FROM opportunity_features").fetchone()[0]
        self.assertEqual(sql_count, len(self.features))


if __name__ == "__main__":
    unittest.main()
