import cirq

def main(minimum_cliffords=5, maximum_cliffords=20, cliffords_step=5):
    simulator = cirq.Simulator()
    q_0 = cirq.GridQubit(0, 0)
    q_1 = cirq.GridQubit(0, 1)
    clifford_range = range(minimum_cliffords, maximum_cliffords, cliffords_step)
    rb_result_1q = cirq.experiments.single_qubit_randomized_benchmarking(
        simulator, q_0, num_clifford_range=clifford_range, repetitions=100
    )
    rb_result_1q.plot()
    rb_result_2q = cirq.experiments.two_qubit_randomized_benchmarking(
        simulator, q_0, q_1, num_clifford_range=clifford_range, repetitions=100
    )
    rb_result_2q.plot()
    cir_1q = cirq.Circuit(cirq.X(q_0) ** 0.5)
    tomography_1q = cirq.experiments.single_qubit_state_tomography(simulator, q_0, cir_1q)
    tomography_1q.plot()
    cir_2q = cirq.Circuit(cirq.H(q_0), cirq.CNOT(q_0, q_1))
    tomography_2q = cirq.experiments.two_qubit_state_tomography(simulator, q_0, q_1, cir_2q)
    tomography_2q.plot()

# Circuit statique pour QSmell (basé sur le circuit de tomographie 2-qubits)
q_0 = cirq.GridQubit(0, 0)
q_1 = cirq.GridQubit(0, 1)
circuit = cirq.Circuit()
circuit.append(cirq.H(q_0))
circuit.append(cirq.CNOT(q_0, q_1))

if __name__ == '__main__':
    main()