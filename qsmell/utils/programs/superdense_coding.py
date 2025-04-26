import cirq

def make_superdense_circuit():
    circuit = cirq.Circuit()
    q0, q1, q2, q3, q4 = cirq.LineQubit.range(5)
    circuit.append([cirq.H(q0), cirq.H(q1)])
    circuit.append(cirq.measure(q0, q1, key="input "))
    circuit.append([cirq.H(q2), cirq.CNOT(q2, q4)])
    circuit.append(cirq.CNOT(q1, q2))
    circuit.append(cirq.CZ(q0, q2))
    circuit.append(cirq.SWAP(q2, q3))
    circuit.append(cirq.CNOT(q3, q4))
    circuit.append(cirq.H(q3))
    circuit.append(cirq.measure(q3, q4, key="output"))
    return circuit

def main():
    circuit = make_superdense_circuit()
    print("Circuit:")
    print(circuit)
    sim = cirq.Simulator()
    results = sim.run(circuit, repetitions=20)
    print("\nResults:")
    print(results)

# Circuit statique pour QSmell
q0, q1, q2, q3, q4 = cirq.LineQubit.range(5)
circuit = cirq.Circuit()
circuit.append([cirq.H(q0), cirq.H(q1)])
circuit.append([cirq.H(q2), cirq.CNOT(q2, q4)])
circuit.append(cirq.CNOT(q1, q2))
circuit.append(cirq.CZ(q0, q2))
circuit.append(cirq.SWAP(q2, q3))
circuit.append(cirq.CNOT(q3, q4))
circuit.append(cirq.H(q3))

if __name__ == '__main__':
    main()