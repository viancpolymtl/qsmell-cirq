""" Usage of customized gates (CG) """

import sys
import pandas as pd
from .ISmell import *

class CG(ISmell):

    def __init__(self):
        super().__init__("CG")

    def is_target_call(pure_name, target_call_name_list, type_name_list, iterable_type):
        return pure_name in target_call_name_list and set(type_name_list).intersection(set(iterable_type))

    def compute_metric(self, df: pd.DataFrame, output_file_path: str) -> None:
        unitary_calls = ['unitary', 'hamiltonian', 'singlequbitunitary']

        metrics = {
            'metric': self._name,
            'value': 0
        }

        qubits = [bit for bit in df.index if bit.startswith('q-')]
        for qubit in qubits:
            row = df.loc[qubit]
            for op in row:
                if op != '':
                    op = op.lower().split('(')[0]
                    if op in unitary_calls:
                        metrics[value] += 1

        out_df = pd.DataFrame.from_dict([metrics])
        sys.stdout.write(str(out_df) + '\n')
        out_df.to_csv(output_file_path, header=True, index=False, mode='w')
