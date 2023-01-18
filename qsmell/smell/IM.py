""" Intermediate measurements (IM) """

import sys
import pandas as pd
from .ISmell import *

class IM(ISmell):

    def __init__(self):
        super().__init__("IM")

    def compute_metric(self, df: pd.DataFrame, output_file_path: str) -> None:
        qubits = [bit for bit in df.index if bit.startswith('q-')]
        stamps = df.columns

        metrics = {
            'metric': self._name,
            'value': 0 # False
        }

        for qubit in qubits:
            if metrics['value'] == 1:
                break
            row = df.loc[qubit]

            is_there_a_measure = False
            for op in row:
                if op == '': # Ignore stamps where the qubit is not used
                    continue
                if op.lower().startswith('barrier'): # Ignore barriers
                    continue

                if op.lower().startswith('measure'):
                    # Found a measure call
                    is_there_a_measure = True
                elif is_there_a_measure:
                    # Found another operation after measure
                    metrics['value'] = 1
                    # No need to continue looking for, as this is at circuit level
                    break

        out_df = pd.DataFrame.from_dict([metrics])
        sys.stdout.write(str(out_df) + '\n')
        out_df.to_csv(output_file_path, header=True, index=False, mode='w')
