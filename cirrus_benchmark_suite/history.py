from pathlib import Path

import pandas as pd

DATA_DIR = Path("data")
STORE_PATH = DATA_DIR / "benchmarks.csv"


class BenchmarkHistory:
    # Non metric columns
    META_COLUMNS = {"id", "datetime", "suite_git_commit", "CIRRUS_version"}

    def __init__(self, source=STORE_PATH, target=STORE_PATH):
        self.data_source = source
        self.data_target = target

        self.reload()

    def update_with(self, metrics):
        new_record = pd.DataFrame([metrics], index=[len(self.benchmarks)])
        self.benchmarks = pd.concat([self.benchmarks, new_record])

        self._save()
        self.reload()

    def _save(self):
        self.data_target.parent.mkdir(parents=True, exist_ok=True)
        self.benchmarks.to_csv(self.data_target, index_label="id")

    def reload(self):
        if self.data_source and self.data_source.exists():
            df = pd.read_csv(self.data_source, index_col="id")
        else:
            df = pd.DataFrame()

        self.benchmarks = df

    @property
    def metrics(self):
        metric_columns = [
            c for c in self.benchmarks.columns if c not in self.META_COLUMNS
        ]
        return self.benchmarks[metric_columns]
