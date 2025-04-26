import random
import numpy as np
import cirq

def make_quantum_teleportation_circuit(ranX, ranY):
    circuit = cirq.Circuit()
    msg, alice, bob = cirq.LineQubit.range(3)
    circuit.append([cirq.H(alice), cirq.CNOT(alice, bob)])
    circuit.append([cirq.X(msg) ** ranX, cirq.Y(msg) ** ranY])
    circuit.append([cirq.CNOT(msg, alice), cirq.H(msg)])
    circuit.append(cirq.measure(msg, key='msg'))
    circuit.append(cirq.measure(alice, key='alice'))
    circuit.append(cirq.X(bob).with_classical_controls('alice'))
    circuit.append(cirq.Z(bob).with_classical_controls('msg'))
    return circuit

def main(seed=None):
    random.seed(seed)
    ranX = random.random()
    ranY = random.random()
    circuit = make_quantum_teleportation_circuit(ranX, ranY)
    print("Circuit:")
    print(circuit)
    sim = cirq.Simulator(seed=seed)
    q0 = cirq.LineQubit(0)
    message = sim.simulate(cirq.Circuit([cirq.X(q0) ** ranX, cirq.Y(q0) ** ranY]))
    print("\nBloch Sphere of Message After Random X and Y Gates:")
    expected = cirq.bloch_vector_from_state_vector(message.final_state_vector, 0)
    print("x: ", np.around(expected[0], 4), "y: ", np.around(expected[1], 4), "z: ", np.around(expected[2], 4))
    final_results = sim.simulate(circuit)
    print("\nBloch Sphere of Qubit 2 at Final State:")
    teleported = cirq.bloch_vector_from_state_vector(final_results.final_state_vector, 2)
    print("x: ", np.around(teleported[0], 4), "y: ", np.around(teleported[1], 4), "z: ", np.around(teleported[2], 4))
    return expected, teleported

# Circuit statique pour QSmell
ranX, ranY = 0.559, 0.647  # Valeurs fixes
msg, alice, bob = cirq.LineQubit.range(3)
circuit = cirq.Circuit()
circuit.append([cirq.H(alice), cirq.CNOT(alice, bob)])
circuit.append([cirq.X(msg) ** ranX, cirq.Y(msg) ** ranY])
circuit.append([cirq.CNOT(msg, alice), cirq.H(msg)])

if __name__ == '__main__':
    main()