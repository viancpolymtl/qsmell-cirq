import itertools
import networkx
import numpy as np
import scipy.optimize
import cirq

def main(repetitions=10, maxiter=50, use_boolean_hamiltonian_gate=False):
    n = 6
    p = 2
    graph = networkx.random_regular_graph(3, n)
    qubits = cirq.LineQubit.range(n)
    betas = np.random.uniform(-np.pi, np.pi, size=p)
    gammas = np.random.uniform(-np.pi, np.pi, size=p)
    circuit = qaoa_max_cut_circuit(qubits, betas, gammas, graph, use_boolean_hamiltonian_gate)
    print('Example QAOA circuit:')
    print(circuit.to_text_diagram(transpose=True))
    largest_cut_found = None
    largest_cut_value_found = 0
    simulator = cirq.Simulator()
    def f(x):
        betas = x[:p]
        gammas = x[p:]
        circuit = qaoa_max_cut_circuit(qubits, betas, gammas, graph, use_boolean_hamiltonian_gate)
        result = simulator.run(circuit, repetitions=repetitions)
        bitstrings = result.measurements['m']
        nonlocal largest_cut_found
        nonlocal largest_cut_value_found
        values = cut_values(bitstrings, graph)
        max_value_index = np.argmax(values)
        max_value = values[max_value_index]
        if max_value > largest_cut_value_found:
            largest_cut_value_found = max_value
            largest_cut_found = bitstrings[max_value_index]
        mean = np.mean(values)
        return -mean
    x0 = np.random.uniform(-np.pi, np.pi, size=2 * p)
    print('Optimizing objective function ...')
    scipy.optimize.minimize(f, x0, method='Nelder-Mead', options={'maxiter': maxiter})
    all_bitstrings = np.array(list(itertools.product(range(2), repeat=n)))
    all_values = cut_values(all_bitstrings, graph)
    max_cut_value = np.max(all_values)
    print(f'The largest cut value found was {largest_cut_value_found}.')
    print(f'The largest possible cut has size {max_cut_value}.')
    print(f'The approximation ratio achieved is {largest_cut_value_found / max_cut_value}.')

def rzz(rads):
    return cirq.ZZPowGate(exponent=2 * rads / np.pi, global_shift=-0.5)

def qaoa_max_cut_unitary(qubits, betas, gammas, graph, use_boolean_hamiltonian_gate):
    if use_boolean_hamiltonian_gate:
        booleans = [f"x{i} ^ x{j}" for i, j in sorted(graph.edges)]
        param_names = [f"x{i}" for i in range(len(qubits))]
        for beta, gamma in zip(betas, gammas):
            yield cirq.BooleanHamiltonianGate(param_names, booleans, 2.0 * gamma).on(*qubits)
            yield cirq.rx(2 * beta).on_each(*qubits)
    else:
        for beta, gamma in zip(betas, gammas):
            yield (rzz(-0.5 * gamma).on(qubits[i], qubits[j]) for i, j in graph.edges)
            yield cirq.rx(2 * beta).on_each(*qubits)

def qaoa_max_cut_circuit(qubits, betas, gammas, graph, use_boolean_hamiltonian_gate):
    return cirq.Circuit(
        cirq.H.on_each(*qubits),
        qaoa_max_cut_unitary(qubits, betas, gammas, graph, use_boolean_hamiltonian_gate),
        cirq.measure(*qubits, key='m'),
    )

def cut_values(bitstrings, graph):
    mat = networkx.adjacency_matrix(graph, nodelist=sorted(graph.nodes))
    vecs = (-1) ** bitstrings
    vals = 0.5 * np.sum(vecs * (mat @ vecs.T).T, axis=-1)
    vals = 0.5 * (graph.size() - vals)
    return vals

# Circuit statique simplifié pour QSmell
n = 4  # Réduit à 4 qubits
p = 1  # Réduit à 1 étape
graph = networkx.Graph()
graph.add_nodes_from(range(n))
graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])  # Graphe cycle simple
q0 = cirq.LineQubit(0)
q1 = cirq.LineQubit(1)
q2 = cirq.LineQubit(2)
q3 = cirq.LineQubit(3)
circuit = cirq.Circuit()
# Étape 1: Hadamard sur tous les qubits
circuit.append(cirq.H(q0))
circuit.append(cirq.H(q1))
circuit.append(cirq.H(q2))
circuit.append(cirq.H(q3))
# Étape 2: ZZ gates pour les arêtes (gamma = -4/13)
gamma = -4/13
exponent = 2 * (-0.5 * gamma) / np.pi
circuit.append(cirq.ZZPowGate(exponent=exponent, global_shift=-0.5).on(q0, q1))
circuit.append(cirq.ZZPowGate(exponent=exponent, global_shift=-0.5).on(q1, q2))
circuit.append(cirq.ZZPowGate(exponent=exponent, global_shift=-0.5).on(q2, q3))
circuit.append(cirq.ZZPowGate(exponent=exponent, global_shift=-0.5).on(q3, q0))
# Étape 3: Rx gates (beta = 0.151 * np.pi)
beta = 0.151 * np.pi
angle = 2 * beta
circuit.append(cirq.rx(angle).on(q0))
circuit.append(cirq.rx(angle).on(q1))
circuit.append(cirq.rx(angle).on(q2))
circuit.append(cirq.rx(angle).on(q3))

if __name__ == '__main__':
    main()