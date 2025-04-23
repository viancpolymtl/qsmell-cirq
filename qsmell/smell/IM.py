""" Intermediate measurements (IM) """

import sys
import pandas as pd
import cirq
from .ISmell import *

class IM(ISmell):

    def __init__(self):
        super().__init__("IM")

    def compute_metric(self, circuit_or_df: cirq.Circuit | pd.DataFrame, output_file_path: str) -> None:
        metrics = {
            'metric': self._name,
            'value': 0  # False
        }

        if isinstance(circuit_or_df, cirq.Circuit):
            all_ops = list(circuit_or_df.all_operations())
            for i, op in enumerate(all_ops[:-1]):  # Exclure la dernière opération
                if isinstance(op.gate, cirq.MeasurementGate):
                    metrics['value'] = 1  # Mesure intermédiaire si suivie d'une autre opération
                    break

        elif isinstance(circuit_or_df, pd.DataFrame):
            qubits = [bit for bit in circuit_or_df.index if bit.startswith('q-')]
            for qubit in qubits:
                row = circuit_or_df.loc[qubit]
                is_there_a_measure = False
                for op in row:
                    if op == '':
                        continue
                    if op.lower().startswith('barrier'):
                        continue
                    if op.lower().startswith('measure'):
                        is_there_a_measure = True
                    elif is_there_a_measure:
                        metrics['value'] = 1
                        break
                if metrics['value'] == 1:
                    break

        out_df = pd.DataFrame.from_dict([metrics])
        sys.stdout.write(str(out_df) + '\n')
        out_df.to_csv(output_file_path, header=True, index=False, mode='w')