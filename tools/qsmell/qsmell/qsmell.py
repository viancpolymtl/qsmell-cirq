""" Main entry point to start using QSmell. """

import ast
import pandas as pd
from qsmell.smell import SmellType

class QSmell:

    def __init__(self):
        pass

    """
    Process a quantum program either as a .py file or .csv file (e.g., as a matrix).

    Attributes:
        smell: Type of smell metric to be computed.
        input_file_path: A string that contains the file local path to be analyzed.
        output_file_path: A string that contains the file local patch for the output.
    """
    def run(self, smell: SmellType, input_file_path: str, output_file_path: str) -> None:
        if input_file_path.endswith('.py'):
            f = open(input_file_path, 'r')
            tree = ast.parse(f.read())
            f.close()
            smell.compute_metric(tree, output_file_path)
        elif input_file_path.endswith('.csv'):
            df = pd.read_csv(input_file_path, sep=';', index_col=0, keep_default_na=False)
            smell.compute_metric(df, output_file_path)
        else:
            raise Exception(input_file_path + ' not supported!')
