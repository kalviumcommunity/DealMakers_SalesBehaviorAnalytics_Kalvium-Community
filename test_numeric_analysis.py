import unittest

import pandas as pd

from src.numeric_analysis import iqr_outliers, zscore_outliers


class ZscoreOutliersTests(unittest.TestCase):
    def test_flags_extreme_value(self):
        values = pd.Series([10, 11, 9, 10, 12, 11, 9, 10, 11, 10, 50000])
        flags = zscore_outliers(values, threshold=3.0)
        self.assertTrue(flags.iloc[-1])
        self.assertFalse(flags.iloc[:-1].any())

    def test_no_flags_for_uniform_values(self):
        values = pd.Series([10.0] * 10)
        flags = zscore_outliers(values)
        self.assertFalse(flags.any())

    def test_nan_is_never_flagged(self):
        values = pd.Series([10, 11, 9, float("nan"), 500])
        flags = zscore_outliers(values, threshold=1.0)
        self.assertFalse(flags.iloc[3])

    def test_preserves_index(self):
        values = pd.Series([1, 2, 3], index=["a", "b", "c"])
        flags = zscore_outliers(values)
        self.assertListEqual(list(flags.index), ["a", "b", "c"])


class IqrOutliersTests(unittest.TestCase):
    def test_flags_value_outside_fences(self):
        values = pd.Series([10, 12, 11, 13, 12, 11, 500])
        flags = iqr_outliers(values)
        self.assertTrue(flags.iloc[-1])
        self.assertFalse(flags.iloc[:-1].any())

    def test_empty_after_dropping_nan_returns_no_flags(self):
        values = pd.Series([float("nan"), float("nan")])
        flags = iqr_outliers(values)
        self.assertFalse(flags.any())

    def test_nan_is_never_flagged(self):
        values = pd.Series([10, 12, 11, 13, float("nan"), 500])
        flags = iqr_outliers(values)
        self.assertFalse(flags.iloc[4])


if __name__ == "__main__":
    unittest.main()
