import random
import cirq

def set_io_qubits(qubit_count):
    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
    output_qubit = cirq.GridQubit(qubit_count, 0)
    return (input_qubits, output_qubit)

def make_oracle(input_qubits, output_qubit, x_bits):
    yield (cirq.X(q) for (q, bit) in zip(input_qubits, x_bits) if not bit)
    yield (cirq.TOFFOLI(input_qubits[0], input_qubits[1], output_qubit))
    yield (cirq.X(q) for (q, bit) in zip(input_qubits, x_bits) if not bit)

def make_grover_circuit(input_qubits, output_qubit, oracle):
    c = cirq.Circuit()
    c.append([cirq.X(output_qubit), cirq.H(output_qubit), cirq.H.on_each(*input_qubits)])
    c.append(oracle)
    c.append(cirq.H.on_each(*input_qubits))
    c.append(cirq.X.on_each(*input_qubits))
    c.append(cirq.H.on(input_qubits[1]))
    c.append(cirq.CNOT(input_qubits[0], input_qubits[1]))
    c.append(cirq.H.on(input_qubits[1]))
    c.append(cirq.X.on_each(*input_qubits))
    c.append(cirq.H.on_each(*input_qubits))
    c.append(cirq.measure(*input_qubits, key='result'))
    return c

def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)

def main():
    qubit_count = 2
    circuit_sample_count = 10
    (input_qubits, output_qubit) = set_io_qubits(qubit_count)
    x_bits = [random.randint(0, 1) for _ in range(qubit_count)]
    print(f'Secret bit sequence: {x_bits}')
    oracle = make_oracle(input_qubits, output_qubit, x_bits)
    circuit = make_grover_circuit(input_qubits, output_qubit, oracle)
    print('Circuit:')
    print(circuit)
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=circuit_sample_count)
    frequencies = result.histogram(key='result', fold_func=bitstring)
    print(f'Sampled results:\n{frequencies}')
    most_common_bitstring = frequencies.most_common(1)[0][0]
    print(f'Most common bitstring: {most_common_bitstring}')
    print(f'Found a match: {most_common_bitstring == bitstring(x_bits)}')

# Circuit statique pour QSmell
qubit_count = 2
input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
output_qubit = cirq.GridQubit(qubit_count, 0)
x_bits = [1, 0]  # Valeurs fixes pour le circuit statique
circuit = cirq.Circuit()
circuit.append([cirq.X(output_qubit), cirq.H(output_qubit)])
circuit.append([cirq.H(q) for q in input_qubits])
# Oracle: décomposé manuellement
if not x_bits[0]:
    circuit.append(cirq.X(input_qubits[0]))
if not x_bits[1]:
    circuit.append(cirq.X(input_qubits[1]))
circuit.append(cirq.TOFFOLI(input_qubits[0], input_qubits[1], output_qubit))
if not x_bits[0]:
    circuit.append(cirq.X(input_qubits[0]))
if not x_bits[1]:
    circuit.append(cirq.X(input_qubits[1]))
# Grover operator
circuit.append([cirq.H(q) for q in input_qubits])
circuit.append([cirq.X(q) for q in input_qubits])
circuit.append(cirq.H(input_qubits[1]))
circuit.append(cirq.CNOT(input_qubits[0], input_qubits[1]))
circuit.append(cirq.H(input_qubits[1]))
circuit.append([cirq.X(q) for q in input_qubits])
circuit.append([cirq.H(q) for q in input_qubits])

if __name__ == '__main__':
    main()