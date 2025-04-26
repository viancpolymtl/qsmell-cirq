import cirq


class Adder(cirq.Gate):
    def __init__(self, num_qubits):
        super(Adder, self)
        self._num_qubits = num_qubits

    def num_qubits(self):
        return self._num_qubits

    def carry(self, *qubits):
        c0, a, b, c1 = qubits
        yield cirq.TOFFOLI(a, b, c1)
        yield cirq.CNOT(a, b)
        yield cirq.TOFFOLI(c0, b, c1)

    def uncarry(self, *qubits):
        c0, a, b, c1 = qubits
        yield cirq.TOFFOLI(c0, b, c1)
        yield cirq.CNOT(a, b)
        yield cirq.TOFFOLI(a, b, c1)

    def carry_sum(self, *qubits):
        c0, a, b = qubits
        yield cirq.CNOT(a, b)
        yield cirq.CNOT(c0, b)

    def _decompose_(self, qubits):
        n = int(len(qubits) / 3)
        c = qubits[0::3]
        a = qubits[1::3]
        b = qubits[2::3]
        for i in range(n - 1):
            yield self.carry(c[i], a[i], b[i], c[i + 1])
        yield self.carry_sum(c[n - 1], a[n - 1], b[n - 1])
        for i in range(n - 2, -1, -1):
            yield self.uncarry(c[i], a[i], b[i], c[i + 1])
            yield self.carry_sum(c[i], a[i], b[i])


class Multiplier(cirq.Gate):
    def __init__(self, num_qubits):
        super(Multiplier, self)
        self._num_qubits = num_qubits

    def num_qubits(self):
        return self._num_qubits

    def _decompose_(self, qubits):
        n = int(len(qubits) / 5)
        a = qubits[1 : n * 3 : 3]
        y = qubits[n * 3 : n * 4]
        x = qubits[n * 4 :]

        for i, x_i in enumerate(x):
            for a_qubit, y_qubit in zip(a[i:], y[: n - i]):
                yield cirq.TOFFOLI(x_i, y_qubit, a_qubit)
            yield Adder(3 * n).on(*qubits[: 3 * n])
            for a_qubit, y_qubit in zip(a[i:], y[: n - i]):
                yield cirq.TOFFOLI(x_i, y_qubit, a_qubit)


def init_qubits(x_bin, *qubits):
    for x, qubit in zip(x_bin, list(qubits)[::-1]):
        if x == '1':
            yield cirq.X(qubit)


def experiment_adder(p, q, n=3):
    a_bin = f'{p:08b}'[-n:]
    b_bin = f'{q:08b}'[-n:]
    qubits = cirq.LineQubit.range(3 * n)
    a = qubits[1::3]
    b = qubits[2::3]
    circuit = cirq.Circuit(
        init_qubits(a_bin, *a),
        init_qubits(b_bin, *b),
        Adder(n * 3).on(*qubits),
        cirq.measure(*b, key='result'),
    )
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1).measurements['result']
    sum_bin = ''.join(result[0][::-1].astype(int).astype(str))
    print(f'{a_bin} + {b_bin} = {sum_bin}')


def experiment_multiplier(p, q, n=3):
    y_bin = f'{p:08b}'[-n:]
    x_bin = f'{q:08b}'[-n:]
    qubits = cirq.LineQubit.range(5 * n)
    b = qubits[2 : n * 3 : 3]
    y = qubits[n * 3 : n * 4]
    x = qubits[n * 4 :]

    circuit = cirq.Circuit(
        init_qubits(x_bin, *x),
        init_qubits(y_bin, *y),
        Multiplier(5 * n).on(*qubits),
        cirq.measure(*b, key='result'),
    )
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)
    sum_bin = ''.join(result.measurements['result'][0][::-1].astype(int).astype(str))
    print(f'{y_bin} * {x_bin} = {sum_bin}')


def main(n=3):
    print('Execute Adder')
    print(cirq.Circuit(cirq.decompose(Adder(3 * n).on(*cirq.LineQubit.range(3 * n)))))
    for p in range(2 * 2):
        for q in range(2 * 2):
            experiment_adder(p, q, n)
    print('')
    print('Execute Multiplier')
    print(cirq.Circuit(cirq.decompose(Multiplier(5 * n).on(*cirq.LineQubit.range(5 * n)))))
    for p in range(2 * 2):
        for q in range(2 * 2):
            experiment_multiplier(p, q, n)


# Circuit statique pour QSmell (décomposé en portes standard)
n = 3
p, q = 0, 0  # Entrées fixes
a_bin = f'{p:08b}'[-n:]
b_bin = f'{q:08b}'[-n:]
qubits = cirq.LineQubit.range(3 * n)
a = qubits[1::3]
b = qubits[2::3]
c = qubits[0::3]

circuit = cirq.Circuit()
# Appliquer init_qubits manuellement
for x, qubit in zip(a_bin, list(a)[::-1]):
    if x == '1':
        circuit.append(cirq.X(qubit))
for x, qubit in zip(b_bin, list(b)[::-1]):
    if x == '1':
        circuit.append(cirq.X(qubit))
# Décomposer Adder manuellement
for i in range(n - 1):
    # Carry: c[i], a[i], b[i], c[i + 1]
    circuit.append(cirq.TOFFOLI(a[i], b[i], c[i + 1]))
    circuit.append(cirq.CNOT(a[i], b[i]))
    circuit.append(cirq.TOFFOLI(c[i], b[i], c[i + 1]))
# Carry sum: c[n-1], a[n-1], b[n-1]
circuit.append(cirq.CNOT(a[n - 1], b[n - 1]))
circuit.append(cirq.CNOT(c[n - 1], b[n - 1]))
for i in range(n - 2, -1, -1):
    # Uncarry: c[i], a[i], b[i], c[i + 1]
    circuit.append(cirq.TOFFOLI(c[i], b[i], c[i + 1]))
    circuit.append(cirq.CNOT(a[i], b[i]))
    circuit.append(cirq.TOFFOLI(a[i], b[i], c[i + 1]))
    # Carry sum: c[i], a[i], b[i]
    circuit.append(cirq.CNOT(a[i], b[i]))
    circuit.append(cirq.CNOT(c[i], b[i]))


if __name__ == '__main__':
    main()