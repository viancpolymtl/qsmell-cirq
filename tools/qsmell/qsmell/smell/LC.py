""" Long circuit (LC) """

import pandas as pd
from .ISmell import *

class LC(ISmell):

    def __init__(self):
        super().__init__("LC")

    def compute_metric(self, df: pd.DataFrame, output_file_path: str) -> None:
        raise Exception(self.name + ' not implemented')
