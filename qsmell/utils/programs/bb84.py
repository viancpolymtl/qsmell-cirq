import cirq
import random

# Logique originale
def main():
    qubits = [cirq.LineQubit(i) for i in range(2)]
    circuit = cirq.Circuit()
    for qubit in qubits:
        if random.choice([0, 1]):
            circuit.append(cirq.H(qubit))
        if random.choice([0, 1]):
            circuit.append(cirq.X(qubit))
    for qubit in qubits:
        if random.choice([0, 1]):
            circuit.append(cirq.H(qubit))
        circuit.append(cirq.measure(qubit, key=f'result_{qubit}'))
    print(circuit)

# Circuit statique pour QSmell
qubits = [cirq.LineQubit(i) for i in range(2)]
circuit = cirq.Circuit()
for qubit in qubits:
    if random.choice([0, 1]):
        circuit.append(cirq.H(qubit))
    if random.choice([0, 1]):
        circuit.append(cirq.X(qubit))
for qubit in qubits:
    if random.choice([0, 1]):
        circuit.append(cirq.H(qubit))

if __name__ == "__main__":
    main()