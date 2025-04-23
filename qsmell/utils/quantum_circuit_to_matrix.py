#!/usr/bin/env python
#
# ------------------------------------------------------------------------------
# Given a cirq.Circuit object, this script "pretty print" it as a coverage matrix.
# Each row represents a quantum bit, each column represents a timestamp in the circuit,
# and each cell represents a quantum operation performed in circuit.
#
# Usage example:
#    from quantum_circuit_to_matrix import Justify, qc2matrix
#
#    import cirq
#    q0, q1 = cirq.NamedQubit('q0'), cirq.NamedQubit('q1')
#    circuit = cirq.Circuit()
#    circuit.append(cirq.H(q0))
#    circuit.append(cirq.CNOT(q0, q1))
#    circuit.append(cirq.measure(q0, key='m0'))
#
#    qc2matrix(circuit, Justify.none, 'example.csv')
#
# Which prints out to the stdout a dataframe and saves it to a CSV file.
# ------------------------------------------------------------------------------

import argparse
import pathlib
import importlib
import sys
import enum
import os

import numpy as np
import pandas as pd
import cirq

# ------------------------------------------------------------ Utility functions

class Justify(enum.Enum):
    left = 'left'
    none = 'none'

    def __str__(self):
        return self.value

def extract_qubit_id(qubit) -> str:
    """Extract a unique ID for a Cirq qubit."""
    return f"q-{qubit.name}" if isinstance(qubit, cirq.NamedQubit) else f"q-{qubit}"

def extract_op_id(operation) -> str:
    """Extract a string representation of a Cirq operation."""
    gate = operation.gate
    if gate is None:
        return "unknown()"
    # Mapper les classes de portes Cirq à des noms simplifiés
    gate_name_map = {
        cirq.HPowGate: 'H',
        cirq.CXPowGate: 'CNOT',
        cirq.CZPowGate: 'CZ',
        cirq.SwapPowGate: 'SWAP',
        cirq.XPowGate: 'X',
        cirq.YPowGate: 'Y',
        cirq.ZPowGate: 'Z',
        cirq.T: 'T',
        cirq.S: 'S',
        cirq.rx: 'Rx',
        cirq.ry: 'Ry',
        cirq.rz: 'Rz',
        cirq.MeasurementGate: 'measure'
    }
    gate_type = type(gate)
    name = gate_name_map.get(gate_type, gate_type.__name__)
    params = [str(p) for p in getattr(gate, 'parameters', [])]
    return f"{name}({','.join(params)})" if params else f"{name}()"

# ------------------------------------------------------------- Module functions

def noalignqc2matrix(circuit: cirq.Circuit) -> pd.DataFrame:
    """Convert a Cirq circuit to a matrix without alignment."""
    qubits = sorted(circuit.all_qubits())
    operations = list(circuit.all_operations())
    
    # Initialize matrix
    nbits = len(qubits)
    depth = len(operations)
    matrix = np.empty((nbits, depth), dtype=str)
    
    col_names = range(1, depth + 1)
    row_names = [extract_qubit_id(q) for q in qubits]
    
    # Initialize DataFrame
    df = pd.DataFrame(matrix, columns=col_names, index=row_names)
    
    # Populate DataFrame
    for col, op in enumerate(operations, 1):
        op_name = extract_op_id(op)
        for qubit in op.qubits:
            df.loc[extract_qubit_id(qubit), col] = op_name
    
    return df

def leftqc2matrix(circuit: cirq.Circuit) -> pd.DataFrame:
    """Convert a Cirq circuit to a matrix with left justification."""
    qubits = sorted(circuit.all_qubits())
    moments = circuit.moments
    
    # Initialize matrix
    nbits = len(qubits)
    depth = len(moments)
    matrix = np.empty((nbits, depth), dtype=str)
    
    col_names = range(1, depth + 1)
    row_names = [extract_qubit_id(q) for q in qubits]
    
    # Initialize DataFrame
    df = pd.DataFrame(matrix, columns=col_names, index=row_names)
    
    # Populate DataFrame based on moments
    for col, moment in enumerate(moments, 1):
        for op in moment.operations:
            op_name = extract_op_id(op)
            for qubit in op.qubits:
                df.loc[extract_qubit_id(qubit), col] = op_name
    
    return df

def qc2matrix(circuit: cirq.Circuit, justify: Justify, output_file_path: str) -> None:
    """Convert a Cirq circuit to a matrix and save it to a CSV file."""
    df = None
    if justify == Justify.none:
        df = noalignqc2matrix(circuit)
    elif justify == Justify.left:
        df = leftqc2matrix(circuit)
    else:
        raise Exception('Unknown justify option ' + str(justify))
    
    sys.stdout.write(str(df) + '\n')
    df.to_csv(output_file_path, header=True, index=True, sep=';', mode='w')

# ------------------------------------------------------------------------- Main

def main():
    parser = argparse.ArgumentParser(description='Convert a Cirq circuit object into a matrix.')
    parser.add_argument('--module-name', '-i', help='Module name that has the Cirq circuit object `circuit`', required=True, type=str)
    parser.add_argument('--justify', '-j', help='`left` (default) or `none`. It refers to where operations should be placed in the output circuit matrix.', required=False, type=Justify, choices=list(Justify), default=Justify.left)
    parser.add_argument('--output-file', '-o', action='store', help='Output file', required=True, type=pathlib.Path)
    args = parser.parse_args()

    module_name: str = args.module_name
    justify: Justify = args.justify
    output_file: str = args.output_file.as_posix()

    # Ajouter le répertoire courant à sys.path pour éviter ModuleNotFoundError
    sys.path.append(os.getcwd())

    wrapper = importlib.import_module(module_name)
    circuit = wrapper.circuit  # Assume the module defines a variable `circuit`
    
    # Process it
    qc2matrix(circuit, justify, output_file)

    sys.exit(0)

if __name__ == "__main__":
    main()