import numpy as np
import pandas as pd

from cirrus_benchmark_suite import evaluate


def test_evaluate_p_value():
    normal = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
    data = pd.DataFrame(
        {
            "A": [*normal, 10],
            "B": [*normal, -10],
            "C": [*normal, 0],
        },
    )

    eval = evaluate.evaluate(data)

    p_values = eval.p_values

    assert p_values["A"] < 0.05  # Well out of normal
    assert p_values["A"] == p_values["B"]  # Opposite side of the disturibution
    assert p_values["C"] == 1.0  # Dead normal


def test_missing_value():
    normal = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
    data = pd.DataFrame(
        {
            "normal": [*normal, 0],
            "missing_new": [*normal, np.nan],
            "missing_some_history": [*normal[:-1], np.nan, 10],
            "missing_all_history": [*([np.nan] * len(normal)), 10],
        },
    )

    eval = evaluate.evaluate(data)

    # Sanity
    assert eval.p_values["normal"] == 1
    assert eval.means["normal"] == 0

    assert not np.isnan(eval.p_values["missing_some_history"])
    assert eval.means["missing_some_history"] == -0.5

    assert np.isnan(eval.p_values["missing_all_history"])
    assert np.isnan(eval.means["missing_all_history"])
    assert np.isnan(eval.stds["missing_all_history"])

    assert "missing_new" not in eval.p_values
