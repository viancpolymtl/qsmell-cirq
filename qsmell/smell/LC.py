""" Long circuit (LC) """

import sys
import pandas as pd
import cirq
from .ISmell import *

class LC(ISmell):

    def __init__(self):
        super().__init__("LC")

    def compute_metric(self, circuit_or_df: cirq.Circuit | pd.DataFrame, output_file_path: str) -> None:
        metrics = {
            'metric': self._name,
            'value': 0
        }

        if isinstance(circuit_or_df, cirq.Circuit):
            max_num_ops_in_any_qubit = max(
                len([op for op in circuit_or_df.all_operations() if q in op.qubits])
                for q in circuit_or_df.all_qubits()
            )
            max_num_ops_in_parallel = max(len(moment.operations) for moment in circuit_or_df.moments)
            metrics['value'] = max_num_ops_in_any_qubit * max_num_ops_in_parallel

        elif isinstance(circuit_or_df, pd.DataFrame):
            df = super().__drop_classical_bits__(circuit_or_df)
            qubits = [bit for bit in df.index if bit.startswith('q-')]
            max_num_ops_in_any_qubit = 0
            for qubit in qubits:
                row = df.loc[qubit]
                max_num_ops_in_any_qubit = max(
                    max_num_ops_in_any_qubit,
                    len([op for op in row if op != '' and not op.lower().startswith('barrier')])
                )
            max_num_ops_in_parallel = 0
            for stamp in df.columns:
                column = df[stamp].tolist()
                max_num_ops_in_parallel = max(
                    max_num_ops_in_parallel,
                    len([op for op in column if op != '' and not op.lower().startswith('barrier')])
                )
            metrics['value'] = max_num_ops_in_any_qubit * max_num_ops_in_parallel

        out_df = pd.DataFrame.from_dict([metrics])
        sys.stdout.write(str(out_df) + '\n')
        out_df.to_csv(output_file_path, header=True, index=False, mode='w')