""" Idle qubits (IdQ) """

import pandas as pd
from .ISmell import *

class IdQ(ISmell):

    def __init__(self):
        super().__init__("IdQ")

    def find_max_consecutive_0(tf_table):
        max_count = 0
        current_count = 0
        for val in tf_table:
            if val == '0':
                current_count += 1
            if val == '1':
                if current_count > max_count:
                    max_count = current_count
                current_count = 0
        return max_count

    def compute_metric(self, df: pd.DataFrame, output_file_path: str) -> None:
        result_list = list()
        for row in content:
            row = row[0]
            row_list = row.split(';')
            row_list = list(filter(lambda x: (x.strip() != ""), row_list))
            tf_table = row[1:]
            if '1' in tf_table:
                first_1_index = tf_table.index('1')
                tf_table = tf_table[first_1_index+1:]
                max_count = find_max_consecutive_0(tf_table)
                result_list.append(max_count)
            else:
                result_list.append(len(tf_table))
        return result_list
