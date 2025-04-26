import numpy as np
import cirq

def main():
    qft_circuit = generate_2x2_grid_qft_circuit()
    print('Circuit:')
    print(qft_circuit)
    simulator = cirq.Simulator()
    result = simulator.simulate(qft_circuit)
    print()
    print('FinalState')
    print(np.around(result.final_state_vector, 3))

def _cz_and_swap(q0, q1, rot):
    yield cirq.CZ(q0, q1) ** rot
    yield cirq.SWAP(q0, q1)

def generate_2x2_grid_qft_circuit():
    a, b, c, d = [
        cirq.GridQubit(0, 0),
        cirq.GridQubit(0, 1),
        cirq.GridQubit(1, 1),
        cirq.GridQubit(1, 0),
    ]
    circuit = cirq.Circuit(
        cirq.H(a),
        _cz_and_swap(a, b, 0.5),
        _cz_and_swap(b, c, 0.25),
        _cz_and_swap(c, d, 0.125),
        cirq.H(a),
        _cz_and_swap(a, b, 0.5),
        _cz_and_swap(b, c, 0.25),
        cirq.H(a),
        _cz_and_swap(a, b, 0.5),
        cirq.H(a),
        strategy=cirq.InsertStrategy.EARLIEST,
    )
    return circuit

# Circuit statique pour QSmell
a, b, c, d = [
    cirq.GridQubit(0, 0),
    cirq.GridQubit(0, 1),
    cirq.GridQubit(1, 1),
    cirq.GridQubit(1, 0),
]
circuit = cirq.Circuit()
circuit.append(cirq.H(a))
circuit.append(cirq.CZ(a, b) ** 0.5)
circuit.append(cirq.SWAP(a, b))
circuit.append(cirq.CZ(b, c) ** 0.25)
circuit.append(cirq.SWAP(b, c))
circuit.append(cirq.CZ(c, d) ** 0.125)
circuit.append(cirq.SWAP(c, d))
circuit.append(cirq.H(a))
circuit.append(cirq.CZ(a, b) ** 0.5)
circuit.append(cirq.SWAP(a, b))
circuit.append(cirq.CZ(b, c) ** 0.25)
circuit.append(cirq.SWAP(b, c))
circuit.append(cirq.H(a))
circuit.append(cirq.CZ(a, b) ** 0.5)
circuit.append(cirq.SWAP(a, b))
circuit.append(cirq.H(a))

if __name__ == '__main__':
    main()