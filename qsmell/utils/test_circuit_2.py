import cirq
q0, q1 = cirq.GridQubit(0, 0), cirq.GridQubit(0, 1)

circuit = cirq.Circuit()
circuit.append(cirq.H(q0))
circuit.append(cirq.X(q1))
circuit.append(cirq.CNOT(q0, q1))