import cirq

# Définir les qubits
n = 2  # Taille du domaine de la fonction
q0 = cirq.LineQubit(0)
q1 = cirq.LineQubit(1)
a0 = cirq.LineQubit(2)
a1 = cirq.LineQubit(3)

# Créer le circuit
circuit = cirq.Circuit()

# Étape 1 : Appliquer H sur les qubits d'entrée
circuit.append(cirq.H(q) for q in [q0, q1])

# Étape 2 : Implémenter une oracle pour une fonction avec une période cachée s = '11'
circuit.append(cirq.CNOT(q0, a0))
circuit.append(cirq.CNOT(q1, a1))
circuit.append(cirq.CNOT(q0, a1))
circuit.append(cirq.CNOT(q1, a1))

# Étape 3 : Appliquer H sur les qubits d’entrée
circuit.append(cirq.H(q) for q in [q0, q1])

# Étape 4 : Mesurer les qubits d'entrée
circuit.append(cirq.measure(q0, q1, key='result'))

# Circuit statique pour QSmell
q0 = cirq.LineQubit(0)
q1 = cirq.LineQubit(1)
a0 = cirq.LineQubit(2)
a1 = cirq.LineQubit(3)
circuit = cirq.Circuit()
# Étape 1 : Hadamard sur les qubits d'entrée
circuit.append(cirq.H(q0))
circuit.append(cirq.H(q1))
# Étape 2 : Oracle pour s = '11'
circuit.append(cirq.CNOT(q0, a0))
circuit.append(cirq.CNOT(q1, a1))
circuit.append(cirq.CNOT(q0, a1))
circuit.append(cirq.CNOT(q1, a1))
# Étape 3 : Hadamard sur les qubits d'entrée
circuit.append(cirq.H(q0))
circuit.append(cirq.H(q1))

if __name__ == '__main__':
    print("Circuit:")
    print(circuit)