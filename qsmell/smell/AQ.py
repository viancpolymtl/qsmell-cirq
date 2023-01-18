""" No-alignment of single and double qubit operations (AQ) """

import pandas as pd
from .ISmell import *

class AQ(ISmell):

    def __init__(self):
        super().__init__("AQ")

    def compute_metric(self, df: pd.DataFrame, output_file_path: str) -> None:
        raise Exception(self.name + ' not implemented')
