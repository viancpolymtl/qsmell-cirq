""" Intermediate measurements (IM) """

import pandas as pd
from .ISmell import *

class IM(ISmell):

    def __init__(self):
        super().__init__("IM")

    def compute_metric(self, df: pd.DataFrame, output_file_path: str) -> None:
        raise Exception(self.name + ' not implemented')
