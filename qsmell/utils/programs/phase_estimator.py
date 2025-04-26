import numpy as np
import cirq

def run_estimate(unknown_gate, qnum, repetitions):
    ancilla = cirq.LineQubit(-1)
    qubits = cirq.LineQubit.range(qnum)
    oracle_raised_to_power = [
        unknown_gate.on(ancilla).controlled_by(qubits[i]) ** (2**i) for i in range(qnum)
    ]
    circuit = cirq.Circuit(
        cirq.H.on_each(*qubits),
        oracle_raised_to_power,
        cirq.qft(*qubits, without_reverse=True) ** -1,
        cirq.measure(*qubits, key='phase'),
    )
    return cirq.sample(circuit, repetitions=repetitions)

def experiment(qnum, repetitions=100):
    def example_gate(phi):
        gate = cirq.MatrixGate(matrix=np.array([[np.exp(2 * np.pi * 1.0j * phi), 0], [0, 1]]))
        return gate
    print(f'Testing with {qnum} qubits.')
    errors = []
    for target in np.arange(0, 1, 0.1):
        result = run_estimate(example_gate(target), qnum, repetitions)
        mode = result.data['phase'].mode()[0]
        guess = mode / 2**qnum
        print(f'target={target:0.4f}, estimate={guess:0.4f}={mode}/{2**qnum}')
        errors.append((target - guess) ** 2)
    rms = np.sqrt(sum(errors) / len(errors))
    print(f'RMS Error: {rms:0.4f}\n')

def main(qnums=(2, 4, 8), repetitions=100):
    for qnum in qnums:
        experiment(qnum, repetitions=repetitions)

# Circuit statique pour QSmell
qnum = 4
ancilla = cirq.LineQubit(-1)
qubits = cirq.LineQubit.range(qnum)
phi = 0.0  # Valeur fixe pour le circuit statique
matrix = np.array([[np.exp(2 * np.pi * 1.0j * phi), 0], [0, 1]])
unknown_gate = cirq.MatrixGate(matrix)
circuit = cirq.Circuit()
circuit.append([cirq.H(q) for q in qubits])
for i in range(qnum):
    circuit.append(unknown_gate.on(ancilla).controlled_by(qubits[i]) ** (2**i))
circuit.append(cirq.qft(*qubits, without_reverse=True) ** -1)

if __name__ == '__main__':
    main()