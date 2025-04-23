""" Repeated set of operations on circuit (ROC) """

import sys
import pandas as pd
import cirq
from .ISmell import *

class ROC(ISmell):

    def __init__(self):
        super().__init__("ROC")

    def compute_metric(self, circuit_or_df: cirq.Circuit | pd.DataFrame, output_file_path: str) -> None:
        metrics = {
            'metric': self._name,
            'value': 0
        }

        if isinstance(circuit_or_df, cirq.Circuit):
            moments = circuit_or_df.moments
            i = 0
            while i < len(moments):
                max_slice_size_with_a_match = 0
                for slice_size in range(1, len(moments) - i):
                    slice_ops = [op for moment in moments[i:i + slice_size] for op in moment.operations]
                    next_slice_ops = [op for moment in moments[i + slice_size:i + 2 * slice_size] for op in moment.operations]
                    if slice_ops == next_slice_ops:
                        metrics['value'] += 1
                        max_slice_size_with_a_match = slice_size
                        break
                i += max_slice_size_with_a_match if max_slice_size_with_a_match > 0 else 1

        elif isinstance(circuit_or_df, pd.DataFrame):
            stamps = circuit_or_df.columns
            i = 0
            while i < len(stamps):
                max_slice_size_with_a_match = 0
                for slice_size in range(1, len(stamps)):
                    slice = []
                    for k in range(0, slice_size):
                        if i + k < len(stamps):
                            slice.extend(circuit_or_df[stamps[i + k]].tolist())
                    next_slice = []
                    for j in range(0, slice_size):
                        if i + k + j + 1 < len(stamps):
                            next_slice.extend(circuit_or_df[stamps[i + k + j + 1]].tolist())
                    if slice == next_slice:
                        print('i %d :: slice_size %d' %(i, slice_size))
                        print('  slice %s == next_slice %s' %(str(slice), str(next_slice)))
                        metrics['value'] += 1
                        max_slice_size_with_a_match = max(max_slice_size_with_a_match, slice_size)
                        break
                i += max_slice_size_with_a_match if max_slice_size_with_a_match > 0 else 1

        out_df = pd.DataFrame.from_dict([metrics])
        sys.stdout.write(str(out_df) + '\n')
        out_df.to_csv(output_file_path, header=True, index=False, mode='w')