from typing import NamedTuple

import numpy as np
import pandas as pd
import scipy.stats


class Evaluation(NamedTuple):
    p_values: pd.Series
    means: pd.Series
    stds: pd.Series
    n_history: int


def evaluate(metrics):
    """
    Generates p_values and statistics based on the last row versus the rest.

    If the last row is missing, the column will be excluded in the
    result.
    """
    last_row = metrics.iloc[-1].astype(float)
    history = metrics.iloc[:-1].astype(float)

    # Filter out missing values
    missing = np.isnan(last_row)
    last_row = last_row[~missing]
    history = history.loc[:, ~missing]

    means = history.mean()
    stds = history.std()

    # Calculate the z-scores for the last row
    z_scores = (last_row - means) / stds

    # Calculate the p-values based on the z-scores
    # Use 2-tailed because we like to know if we speed things up significantly
    p_values = z_scores.apply(lambda z: scipy.stats.norm.sf(abs(z)) * 2)

    return Evaluation(p_values, means, stds, n_history=history.count())
