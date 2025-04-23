# test_circuit.py
import cirq

q0, q1 = cirq.NamedQubit('q0'), cirq.NamedQubit('q1')
circuit = cirq.Circuit()
circuit.append(cirq.H(q0))  # IQ: initialisation non-|0⟩
circuit.append(cirq.CNOT(q0, q1))  # CG: pas de porte personnalisée
circuit.append(cirq.measure(q0, key='m0'))  # IM: mesure intermédiaire
circuit.append(cirq.H(q1))  # IM: opération après mesure