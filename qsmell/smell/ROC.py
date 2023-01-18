""" Repeated set of operations on circuit (ROC) """

import sys
import pandas as pd
from .ISmell import *

class ROC(ISmell):

    def __init__(self):
        super().__init__("ROC")

    def compute_metric(self, df: pd.DataFrame, output_file_path: str) -> None:
        stamps = df.columns

        num_repetitions = 0
        i = 0
        while i < len(stamps):
            stamp = stamps[i]

            max_slice_size_with_a_match = 0
            for slice_size in range(1, len(stamps)):

                # Current slice is composed by the column pointed by `i`
                slice = []
                # Augment current `slice` with as many columns as the `slice_size`
                for k in range(0, slice_size):
                    if i+k < len(stamps):
                        slice.extend(df[stamps[i+k]].tolist())

                # Get next slice of columns
                next_slice = []
                for j in range(0, slice_size):
                    if i+k+j+1 < len(stamps):
                        next_slice.extend(df[stamps[i+k+j+1]].tolist())

                # Check whether current slice is equal to the following slice
                if slice == next_slice:
                    print('i %d :: slice_size %d' %(i, slice_size)) # debug
                    print('  slice %s == next_slice %s' %(str(slice), str(next_slice))) # debug
                    num_repetitions += 1
                    max_slice_size_with_a_match = max(max_slice_size_with_a_match, slice_size)
                    break

            i += max_slice_size_with_a_match if max_slice_size_with_a_match > 0 else 1

        metrics = {
            'metric': self._name,
            'value': num_repetitions
        }

        out_df = pd.DataFrame.from_dict([metrics])
        sys.stdout.write(str(out_df) + '\n')
        out_df.to_csv(output_file_path, header=True, index=False, mode='w')
