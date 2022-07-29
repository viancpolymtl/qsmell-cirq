""" Repeated set of operations on circuit (ROC) """

import pandas as pd
from .ISmell import *

class ROC(ISmell):

    def __init__(self):
        super().__init__("ROC")

    def compute_metric(self, df: pd.DataFrame, output_file_path: str) -> None:
        raise Exception(self.name + ' not implemented')
