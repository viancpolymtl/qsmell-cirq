""" Long circuit (LC) """

import sys
import pandas as pd
from .ISmell import *

class LC(ISmell):

    def __init__(self):
        super().__init__("LC")

    def compute_metric(self, df: pd.DataFrame, output_file_path: str) -> None:
        qubits = [bit for bit in df.index if bit.startswith('q-')]
        stamps = df.columns

        max_num_ops_in_any_qubit = 0
        for qubit in qubits:
            row = df.loc[qubit]
            max_num_ops_in_any_qubit = max(max_num_ops_in_any_qubit, len([op for op in row if op != '']))

        max_num_ops_in_parallel = 0
        for stamp in stamps:
            column = df[stamp]
            max_num_ops_in_parallel = max(max_num_ops_in_parallel, len([op for op in column if op != '']))

        metric = max_num_ops_in_any_qubit * max_num_ops_in_parallel

        out_df = pd.DataFrame.from_dict([{'lc': metric}])
        sys.stdout.write(str(out_df) + '\n')
        out_df.to_csv(output_file_path, header=True, index=False, mode='w')
