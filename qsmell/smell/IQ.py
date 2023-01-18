""" Initialization of qubits differently from |0⟩ (IQ) """

import sys
import pandas as pd
from .ISmell import *

class IQ(ISmell):

    def __init__(self):
        super().__init__("IQ")

    def compute_metric(self, df: pd.DataFrame, output_file_path: str) -> None:
        qubits = [bit for bit in df.index if bit.startswith('q-')]
        stamps = df.columns

        metrics = {
            'metric': self._name,
            'value': 0
        }

        for qubit in qubits:
            max_num_ops_between_init_and_use = 0
            count = -1
            for stamp in stamps:
                op = df.loc[qubit][stamp]
                if op.lower().startswith('barrier'): # Ignore barriers
                    continue

                if op == '' and count == -1:
                    # The first operation on qubit has not been found yet
                    pass
                elif op != '' and count == -1:
                    # Found the first operation on qubit
                    count = 0
                elif op != '' and count != -1:
                    # Found the second operation on qubit
                    max_num_ops_between_init_and_use = max(max_num_ops_between_init_and_use, count)
                    break
                elif op == '' and count != -1:
                    # Empty operation in between
                    count += 1

            metrics['value'] = max(metrics['value'], max_num_ops_between_init_and_use)

        out_df = pd.DataFrame.from_dict([metrics])
        sys.stdout.write(str(out_df) + '\n')
        out_df.to_csv(output_file_path, header=True, index=False, mode='w')
