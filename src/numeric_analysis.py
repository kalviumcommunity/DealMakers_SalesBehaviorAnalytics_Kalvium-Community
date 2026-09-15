"""Vectorised NumPy helpers for statistical outlier detection.

Pandas covers most of this pipeline's transformations, but outlier flagging
is done with NumPy directly: nanmean/nanstd/nanpercentile give a single
vectorised pass over the array instead of a Python loop, and NaNs (open
opportunities with no close_value) are preserved rather than dropped.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def zscore_outliers(values: pd.Series, threshold: float = 3.0) -> pd.Series:
    """Flag values whose absolute z-score exceeds the threshold. NaNs are never flagged."""
    numeric = values.astype(float).to_numpy()
    mean = np.nanmean(numeric)
    std = np.nanstd(numeric)
    if std == 0 or np.isnan(std):
        flags = np.zeros(len(numeric), dtype=bool)
    else:
        z_scores = np.abs((numeric - mean) / std)
        flags = np.nan_to_num(z_scores, nan=0.0) > threshold
    return pd.Series(flags, index=values.index)


def iqr_outliers(values: pd.Series, multiplier: float = 1.5) -> pd.Series:
    """Flag values outside [Q1 - multiplier*IQR, Q3 + multiplier*IQR]. NaNs are never flagged."""
    numeric = values.astype(float).to_numpy()
    finite = numeric[~np.isnan(numeric)]
    if finite.size == 0:
        return pd.Series(np.zeros(len(numeric), dtype=bool), index=values.index)
    q1, q3 = np.nanpercentile(numeric, [25, 75])
    iqr = q3 - q1
    lower, upper = q1 - multiplier * iqr, q3 + multiplier * iqr
    flags = (numeric < lower) | (numeric > upper)
    return pd.Series(flags, index=values.index)
