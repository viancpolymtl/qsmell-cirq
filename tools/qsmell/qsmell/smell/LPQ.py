""" No-alignment between the logical and physical qubits (LPQ) """

import sys
import ast
import pandas as pd
from .ISmell import *

class LPQ(ISmell):

    def __init__(self):
        super().__init__("LPQ")

    def compute_metric(self, tree: ast.Module, output_file_path: str) -> None:
        raise Exception(self.name + ' not implemented')
