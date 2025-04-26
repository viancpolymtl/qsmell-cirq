import random
import cirq

def set_qubits(qubit_count):
    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
    return input_qubits

def make_oracle_f(qubits):
    return [cirq.CZ(qubits[2 * i], qubits[2 * i + 1]) for i in range(len(qubits) // 2)]

def make_hs_circuit(qubits, oracle_f, shift):
    c = cirq.Circuit()
    c.append([cirq.H.on_each(*qubits)])
    c.append([cirq.X.on_each([qubits[k] for k in range(len(shift)) if shift[k]])])
    c.append(oracle_f)
    c.append([cirq.X.on_each([qubits[k] for k in range(len(shift)) if shift[k]])])
    c.append([cirq.H.on_each(*qubits)])
    c.append(oracle_f)
    c.append([cirq.H.on_each(*qubits)])
    c.append(cirq.measure(*qubits, key='result'))
    return c

def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)

def main():
    qubit_count = 6
    sample_count = 100
    input_qubits = set_qubits(qubit_count)
    shift = [random.randint(0, 1) for _ in range(qubit_count)]
    print(f'Secret shift sequence: {shift}')
    oracle_f = make_oracle_f(input_qubits)
    circuit = make_hs_circuit(input_qubits, oracle_f, shift)
    print('Circuit:')
    print(circuit)
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=sample_count)
    frequencies = result.histogram(key='result', fold_func=bitstring)
    print(f'Sampled results:\n{frequencies}')
    most_common_bitstring = frequencies.most_common(1)[0][0]
    print(f'Most common bitstring: {most_common_bitstring}')
    print(f'Found a match: {most_common_bitstring == bitstring(shift)}')

# Circuit statique simplifié pour QSmell
qubit_count = 4  # Réduit à 4 qubits pour simplifier
input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
shift = [1, 0, 0, 1]  # Valeurs fixes adaptées
circuit = cirq.Circuit()
# Étape 1: Hadamard sur tous les qubits
circuit.append([cirq.H(input_qubits[0]), cirq.H(input_qubits[1]), cirq.H(input_qubits[2]), cirq.H(input_qubits[3])])
# Étape 2: Shift (X gates)
circuit.append([cirq.X(input_qubits[0]), cirq.X(input_qubits[3])])
# Étape 3: Oracle f (CZ gates)
circuit.append([cirq.CZ(input_qubits[0], input_qubits[1]), cirq.CZ(input_qubits[2], input_qubits[3])])
# Étape 4: Shift (X gates)
circuit.append([cirq.X(input_qubits[0]), cirq.X(input_qubits[3])])
# Étape 5: Hadamard
circuit.append([cirq.H(input_qubits[0]), cirq.H(input_qubits[1]), cirq.H(input_qubits[2]), cirq.H(input_qubits[3])])
# Étape 6: Oracle f (CZ gates)
circuit.append([cirq.CZ(input_qubits[0], input_qubits[1]), cirq.CZ(input_qubits[2], input_qubits[3])])
# Étape 7: Hadamard final
circuit.append([cirq.H(input_qubits[0]), cirq.H(input_qubits[1]), cirq.H(input_qubits[2]), cirq.H(input_qubits[3])])

if __name__ == '__main__':
    main()