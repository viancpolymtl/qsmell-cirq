""" No-alignment of single and double qubit operations (AQ) """

import sys
import pandas as pd
import cirq
from .ISmell import *

class AQ(ISmell):

    def __init__(self):
        super().__init__("AQ")

    def compute_metric(self, circuit_or_df: cirq.Circuit | pd.DataFrame, output_file_path: str) -> None:
        metrics = {
            'metric': self._name,
            'value': 0
        }

        if isinstance(circuit_or_df, cirq.Circuit):
            for moment in circuit_or_df.moments:
                has_measurement = False
                has_single_qubit_gate = False
                has_two_qubit = False
                for op in moment.operations:
                    if isinstance(op.gate, cirq.MeasurementGate):
                        has_measurement = True
                    elif len(op.qubits) == 1:
                        has_single_qubit_gate = True
                    elif len(op.qubits) == 2:
                        has_two_qubit = True
                # Mélange de mesure et porte à un qubit, ou mesure et porte à deux qubits, ou un/deux qubits
                if (has_measurement and (has_single_qubit_gate or has_two_qubit)) or \
                   (has_single_qubit_gate and has_two_qubit):
                    metrics['value'] += 1

        elif isinstance(circuit_or_df, pd.DataFrame):
            df = super().__drop_barriers__(circuit_or_df)
            for col in df.columns:
                ops = df[col].tolist()
                has_measurement = any(op.lower().startswith('measure') for op in ops if op)
                has_single_qubit = any(op != '' and op not in ['CNOT()', 'CZ()', 'SWAP()', 'measure()'] 
                                     and not op.lower().startswith('measure') for op in ops)
                has_two_qubit = any(op in ['CNOT()', 'CZ()', 'SWAP()'] for op in ops)
                if (has_measurement and (has_single_qubit or has_two_qubit)) or \
                   (has_single_qubit and has_two_qubit):
                    metrics['value'] += 1

        out_df = pd.DataFrame.from_dict([metrics])
        sys.stdout.write(str(out_df) + '\n')
        out_df.to_csv(output_file_path, header=True, index=False, mode='w')