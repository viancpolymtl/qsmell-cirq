import cirq

# Définir les qubits
n = 3  # Nombre de qubits pour la fonction
qubits = [cirq.LineQubit(i) for i in range(n)]
oracle_qubit = cirq.LineQubit(n)

# Créer le circuit
circuit = cirq.Circuit()

# Étape 1 : Appliquer H sur tous les qubits d'entrée et un X suivi de H sur le qubit oracle
circuit.append(cirq.H(q) for q in qubits)
circuit.append(cirq.X(oracle_qubit))
circuit.append(cirq.H(oracle_qubit))

# Étape 2 : Implémenter une oracle équilibrée (par exemple, f(x) = x_0 XOR x_1)
# Ici, on utilise des CNOT pour simuler une fonction équilibrée
circuit.append(cirq.CNOT(qubits[0], oracle_qubit))
circuit.append(cirq.CNOT(qubits[1], oracle_qubit))

# Étape 3 : Appliquer H sur les qubits d'entrée
circuit.append(cirq.H(q) for q in qubits)

# Étape 4 : Mesurer les qubits d'entrée
circuit.append(cirq.measure(*qubits, key='result'))