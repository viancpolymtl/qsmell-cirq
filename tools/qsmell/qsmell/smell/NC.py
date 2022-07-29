""" Non-parameterized circuit (NC) """

import pandas as pd
from .ISmell import *

class NC(ISmell):

    def __init__(self):
        super().__init__("NC")

    def compute_metric(self, df: pd.DataFrame, output_file_path: str) -> None:
        raise Exception(self.name + ' not implemented')
