""" Main entry point to start using QSmell. """

import pandas as pd
from qsmell.smell import SmellType

class QSmell:

    def __init__(self):
        pass

    """
    Process a quantum circuit as a matrix.

    Attributes:
        smell: Type of smell metric to be computed.
        input_file_path: A string that contains the file local path to be analyzed.
        output_file_path: A string that contains the file local patch for the output.
    """
    def run(self, smell: SmellType, input_file_path: str, output_file_path: str) -> None:
        df = pd.read_csv(input_file_path, sep=';', index_col=0)
        smell.compute_metric(df, output_file_path)
