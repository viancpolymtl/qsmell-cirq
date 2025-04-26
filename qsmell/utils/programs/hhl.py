import math
import numpy as np
import sympy
import cirq

class PhaseEstimation(cirq.Gate):
    def __init__(self, num_qubits, unitary):
        self._num_qubits = num_qubits
        self.U = unitary

    def num_qubits(self):
        return self._num_qubits

    def _decompose_(self, qubits):
        qubits = list(qubits)
        yield cirq.H.on_each(*qubits[:-1])
        yield PhaseKickback(self.num_qubits(), self.U)(*qubits)
        yield cirq.qft(*qubits[:-1], without_reverse=True) ** -1

class HamiltonianSimulation(cirq.EigenGate):
    def __init__(self, A, t, exponent=1.0):
        cirq.EigenGate.__init__(self, exponent=exponent)
        self.A = A
        self.t = t
        ws, vs = np.linalg.eigh(A)
        self.eigen_components = []
        for w, v in zip(ws, vs.T):
            theta = w * t / math.pi
            P = np.outer(v, np.conj(v))
            self.eigen_components.append((theta, P))

    def _num_qubits_(self) -> int:
        return 1

    def _with_exponent(self, exponent):
        return HamiltonianSimulation(self.A, self.t, exponent)

    def _eigen_components(self):
        return self.eigen_components

class PhaseKickback(cirq.Gate):
    def __init__(self, num_qubits, unitary):
        super(PhaseKickback, self)
        self._num_qubits = num_qubits
        self.U = unitary

    def num_qubits(self):
        return self._num_qubits

    def _decompose_(self, qubits):
        qubits = list(qubits)
        memory = qubits.pop()
        for i, qubit in enumerate(qubits):
            yield cirq.ControlledGate(self.U ** (2**i))(qubit, memory)

class EigenRotation(cirq.Gate):
    def __init__(self, num_qubits, C, t):
        super(EigenRotation, self)
        self._num_qubits = num_qubits
        self.C = C
        self.t = t
        self.N = 2 ** (num_qubits - 1)

    def num_qubits(self):
        return self._num_qubits

    def _decompose_(self, qubits):
        for k in range(self.N):
            kGate = self._ancilla_rotation(k)
            xor = k ^ (k - 1)
            for q in qubits[-2::-1]:
                if xor % 2 == 1:
                    yield cirq.X(q)
                xor >>= 1
                kGate = cirq.ControlledGate(kGate)
            yield kGate(*qubits)

    def _ancilla_rotation(self, k):
        if k == 0:
            k = self.N
        theta = 2 * math.asin(self.C * self.N * self.t / (2 * math.pi * k))
        return cirq.ry(theta)

def hhl_circuit(A, C, t, register_size, *input_prep_gates):
    ancilla = cirq.LineQubit(0)
    register = [cirq.LineQubit(i + 1) for i in range(register_size)]
    memory = cirq.LineQubit(register_size + 1)
    c = cirq.Circuit()
    hs = HamiltonianSimulation(A, t)
    pe = PhaseEstimation(register_size + 1, hs)
    c.append([gate(memory) for gate in input_prep_gates])
    c.append([
        pe(*(register + [memory])),
        EigenRotation(register_size + 1, C, t)(*(register + [ancilla])),
        pe(*(register + [memory])) ** -1,
        cirq.measure(ancilla, key='a'),
    ])
    c.append([
        cirq.PhasedXPowGate(exponent=sympy.Symbol('exponent'), phase_exponent=sympy.Symbol('phase_exponent'))(memory),
        cirq.measure(memory, key='m'),
    ])
    return c

def simulate(circuit):
    simulator = cirq.Simulator()
    params = [
        {'exponent': 0.5, 'phase_exponent': -0.5},
        {'exponent': 0.5, 'phase_exponent': 0},
        {'exponent': 0, 'phase_exponent': 0},
    ]
    results = simulator.run_sweep(circuit, params, repetitions=5000)
    for label, result in zip(('X', 'Y', 'Z'), list(results)):
        expectation = 1 - 2 * np.mean(result.measurements['m'][result.measurements['a'] == 1])
        print(f'{label} = {expectation}')

def main():
    A = np.array([
        [4.30213466 - 6.01593490e-08j, 0.23531802 + 9.34386156e-01j],
        [0.23531882 - 9.34388383e-01j, 0.58386534 + 6.01593489e-08j],
    ])
    t = 0.358166 * math.pi
    register_size = 4
    input_prep_gates = [cirq.rx(1.276359), cirq.rz(1.276359)]
    expected = (0.144130, 0.413217, -0.899154)
    C = 2 * math.pi / (2**register_size * t)
    print("Expected observable outputs:")
    print("X =", expected[0])
    print("Y =", expected[1])
    print("Z =", expected[2])
    print("Actual: ")
    simulate(hhl_circuit(A, C, t, register_size, *input_prep_gates))

# Circuit statique pour QSmell (simplifié et décomposé)
register_size = 2  # Réduit pour simplifier
ancilla = cirq.LineQubit(0)
register = [cirq.LineQubit(i + 1) for i in range(register_size)]
memory = cirq.LineQubit(register_size + 1)
circuit = cirq.Circuit()
# Préparation de l'entrée
circuit.append([cirq.rx(1.276359)(memory), cirq.rz(1.276359)(memory)])
# Phase estimation (simplifiée)
circuit.append([cirq.H(q) for q in register])
# Phase kickback simulé (sans HamiltonianSimulation)
for i, qubit in enumerate(register):
    circuit.append(cirq.ControlledGate(cirq.Z ** (2**i))(qubit, memory))
# QFT inverse simplifiée
circuit.append(cirq.qft(*register, without_reverse=True) ** -1)
# EigenRotation (simplifiée pour k=1)
theta = 2 * math.asin((2 * math.pi / (2**register_size * 0.358166 * math.pi)) * (2**register_size) * (0.358166 * math.pi) / (2 * math.pi * 1))
circuit.append(cirq.ry(theta)(ancilla))

if __name__ == '__main__':
    main()