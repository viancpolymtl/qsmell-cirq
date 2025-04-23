""" Idle qubits (IdQ) """

import sys
import pandas as pd
import cirq
from .ISmell import *

class IdQ(ISmell):

    def __init__(self):
        super().__init__("IdQ")

    def compute_metric(self, circuit_or_df: cirq.Circuit | pd.DataFrame, output_file_path: str) -> None:
        metrics = {
            'metric': self._name,
            'value': 0
        }

        if isinstance(circuit_or_df, cirq.Circuit):
            if circuit_or_df.moments:
                first_moment = circuit_or_df.moments[0]
                active_qubits = {q for op in first_moment.operations for q in op.qubits}
                all_qubits = circuit_or_df.all_qubits()
                for qubit in all_qubits:
                    if qubit not in active_qubits:
                        metrics['value'] += 1

        elif isinstance(circuit_or_df, pd.DataFrame):
            qubits = [bit for bit in circuit_or_df.index if bit.startswith('q-')]
            for qubit in qubits:
                row = circuit_or_df.loc[qubit]
                first_op_idx = next((i for i, op in enumerate(row) if op), len(row))
                if first_op_idx > 0:
                    metrics['value'] += 1

        out_df = pd.DataFrame.from_dict([metrics])
        sys.stdout.write(str(out_df) + '\n')
        out_df.to_csv(output_file_path, header=True, index=False, mode='w')