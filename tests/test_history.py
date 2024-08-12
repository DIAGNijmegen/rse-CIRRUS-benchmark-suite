import os
from pathlib import Path

from cirrus_benchmark_suite.history import BenchmarkHistory

SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
RESOURCE_PATH = SCRIPT_DIR / Path("resources")


def test_loading():
    history = BenchmarkHistory(source=RESOURCE_PATH / "benchmarks.csv")
    bms = history.benchmarks
    assert len(bms) == 3
    assert list(bms.index) == [0, 1, 2]
    assert bms.index.name == "id"


def test_add(tmp_path):
    save_target = Path(tmp_path) / "data" / "test.csv"
    history = BenchmarkHistory(source=None, target=save_target)
    history.update_with(dict(a_metric=1))

    new_history = BenchmarkHistory(source=save_target)

    record = new_history.benchmarks.iloc[0]
    assert record["a_metric"] == 1


def test_metrics_only():
    history = BenchmarkHistory(source=RESOURCE_PATH / "benchmarks.csv")
    metrics = history.metrics

    assert len(metrics) == 3
    assert list(metrics.index) == [0, 1, 2]
    assert len(metrics.columns) == 4
