""" Initial qubit state (IQ) """

import sys
import pandas as pd
import cirq
from .ISmell import *

class IQ(ISmell):

    def __init__(self):
        super().__init__("IQ")

    def compute_metric(self, circuit_or_df: cirq.Circuit | pd.DataFrame, output_file_path: str) -> None:
        metrics = {
            'metric': self._name,
            'value': 0
        }

        if isinstance(circuit_or_df, cirq.Circuit):
            if circuit_or_df.moments:  # Vérifier si la liste des moments n'est pas vide
                first_moment = circuit_or_df.moments[0]
                for op in first_moment.operations:
                    if not isinstance(op.gate, cirq.IdentityGate):
                        metrics['value'] += 1

        elif isinstance(circuit_or_df, pd.DataFrame):
            qubits = [bit for bit in circuit_or_df.index if bit.startswith('q-')]
            for qubit in qubits:
                row = circuit_or_df.loc[qubit]
                for op in row:
                    if op == '':
                        continue
                    if op.lower().startswith('barrier'):
                        continue
                    if not op.lower().startswith('i'):
                        metrics['value'] += 1
                    break

        out_df = pd.DataFrame.from_dict([metrics])
        sys.stdout.write(str(out_df) + '\n')
        out_df.to_csv(output_file_path, header=True, index=False, mode='w')