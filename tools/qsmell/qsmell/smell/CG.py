""" Usage of customized gates (CG) """

import pandas as pd
from .ISmell import *

class CG(ISmell):

    def __init__(self):
        super().__init__("CG")

    def compute_metric(self, df: pd.DataFrame, output_file_path: str) -> None:
        raise Exception(self.name + ' not implemented')
