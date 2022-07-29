""" Idle qubits (IdQ) """

import pandas as pd
from .ISmell import *

class IdQ(ISmell):

    def __init__(self):
        super().__init__("IdQ")

    def compute_metric(self, df: pd.DataFrame, output_file_path: str) -> None:
        raise Exception(self.name + ' not implemented')
