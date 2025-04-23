""" Usage of customized gates (CG) """

import sys
import pandas as pd
import cirq
from .ISmell import *

class CG(ISmell):

    def __init__(self):
        super().__init__("CG")

    def compute_metric(self, circuit_or_df: cirq.Circuit | pd.DataFrame, output_file_path: str) -> None:
        metrics = {
            'metric': self._name,
            'value': 0
        }

        if isinstance(circuit_or_df, cirq.Circuit):
            for op in circuit_or_df.all_operations():
                if isinstance(op.gate, cirq.Gate) and not self._is_standard_gate(op.gate):
                    metrics['value'] += 1

        elif isinstance(circuit_or_df, pd.DataFrame):
            qubits = [bit for bit in circuit_or_df.index if bit.startswith('q-')]
            for qubit in qubits:
                row = circuit_or_df.loc[qubit]
                for op in row:
                    if op and not self._is_standard_operation(op):
                        metrics['value'] += 1

        out_df = pd.DataFrame.from_dict([metrics])
        sys.stdout.write(str(out_df) + '\n')
        out_df.to_csv(output_file_path, header=True, index=False, mode='w')

    def _is_standard_gate(self, gate):
        """Check if a gate is standard in Cirq."""
        standard_gates = [
            cirq.HPowGate, cirq.XPowGate, cirq.YPowGate, cirq.ZPowGate,
            cirq.CXPowGate, cirq.CZPowGate, cirq.SwapPowGate,
            cirq.MeasurementGate,
            type(cirq.T), type(cirq.S)  # Gérer T et S via leurs types
        ]
        return isinstance(gate, tuple(standard_gates))

    def _is_standard_operation(self, op_name: str) -> bool:
        """Check if an operation name corresponds to a standard gate."""
        standard_ops = ['H', 'X', 'Y', 'Z', 'CNOT', 'CZ', 'SWAP', 'T', 'S', 'Rx', 'Ry', 'Rz', 'measure']
        return op_name and any(op_name.startswith(op) for op in standard_ops)