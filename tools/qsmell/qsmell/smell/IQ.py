""" Initialization of qubits differently from |0⟩ (IQ) """

import pandas as pd
from .ISmell import *

class IQ(ISmell):

    def __init__(self):
        super().__init__("IQ")

    def compute_metric(self, df: pd.DataFrame, output_file_path: str) -> None:
        raise Exception(self.name + ' not implemented')
