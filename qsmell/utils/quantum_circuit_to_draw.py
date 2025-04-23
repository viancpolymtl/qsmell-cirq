#!/usr/bin/env python
#
# ------------------------------------------------------------------------------
# Given a [qiskit.circuit.QuantumCircuit](https://qiskit.org/documentation/apidoc/circuit.html)
# object, this script "pretty print" it as a draw.
#
# Usage example:
#    python quantum_circuit_to_draw.py
#        --module-name <str, e.g., wrapper_adapt_vqe>
#        --output-type <str, i.e., text, latex_source, or mpl>
#        --output-file <path, e.g., adapt_vqe.txt>
# ------------------------------------------------------------------------------

import argparse
import pathlib
import importlib
import sys
import cirq

def main():
    parser = argparse.ArgumentParser(description='Convert a Cirq circuit object into a text diagram.')
    parser.add_argument('--module-name', '-i', help='Module name that has the Cirq circuit object `circuit`', required=True, type=str)
    parser.add_argument('--output-file', '-o', action='store', help='Output file', required=True, type=pathlib.Path)
    args = parser.parse_args()

    module_name: str = args.module_name
    output_file: str = args.output_file.as_posix()

    wrapper = importlib.import_module(module_name)
    circuit = wrapper.circuit  # Assume the module defines a variable `circuit`
    
    # Draw the circuit as a text diagram
    with open(output_file, 'w') as f:
        f.write(circuit.to_text_diagram())

    sys.exit(0)

if __name__ == "__main__":
    main()

# EOF
