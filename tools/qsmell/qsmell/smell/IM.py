""" Intermediate measurements (IM) """

import pandas as pd
from .ISmell import *

class IM(ISmell):

    def __init__(self):
        super().__init__("IM")

    def compute_metric(self, df: pd.DataFrame, output_file_path: str) -> None:
        call_split_list = title.split(';')
        call_split_list = list(filter(lambda x: (x.strip() != ""), call_split_list))
        pure_call_name_list = list()
        for call in call_split_list:
            pure_call_name_list.append(call.split("(", 1)[0].strip())
        if 'measure' in pure_call_name_list:
            first_measure_index = pure_call_name_list.index('measure')
            sublist = pure_call_name_list[first_measure_index+1:]
            for sub_call in sublist:
                if sub_call != 'measure':
                    return True
            return False
        else:
            return False
