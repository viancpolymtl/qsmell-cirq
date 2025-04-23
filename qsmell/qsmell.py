""" Main entry point to start using QSmell. """

import ast
import pandas as pd
import cirq
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
            with open(input_file_path, 'r') as f:
                code = f.read()
            tree = ast.parse(code)
            local_vars = {}
            exec(code, {'cirq': cirq}, local_vars)
            circuits = [obj for obj in local_vars.values() if isinstance(obj, cirq.Circuit)]
            if not circuits:
                raise Exception("No cirq.Circuit found in the input file!")
            if smell.name in ['LPQ', 'NC']:
                smell.compute_metric_ast(tree, output_file_path)
            else:
                smell.compute_metric(circuits[0], output_file_path)
        elif input_file_path.endswith('.csv'):
            df = pd.read_csv(input_file_path, sep=';', index_col=0, keep_default_na=False)
            smell.compute_metric(df, output_file_path)
        else:
            raise Exception(input_file_path + ' not supported!')