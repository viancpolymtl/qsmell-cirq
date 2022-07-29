""" No-alignment between the logical and physical qubits (LPQ) """

import pandas as pd
from .ISmell import *

class LPQ(ISmell):

    def __init__(self):
        super().__init__("LPQ")

    def compute_metric(self, df: pd.DataFrame, output_file_path: str) -> None:
        raise Exception(self.name + ' not implemented')
