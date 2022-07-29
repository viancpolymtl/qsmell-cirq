""" Smell interface. """

import pandas as pd

class ISmell:

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def compute_metric(self, df: pd.DataFrame, output_file_path: str) -> None:
        raise Exception('Not implemented')

    def __str__(self) -> str:
        return self.name
