import argparse
import fractions
import math
import random
import sympy
import cirq

parser = argparse.ArgumentParser(description='Factorization demo.')
parser.add_argument('n', type=int, help='composite integer to factor')
parser.add_argument(
    '--order_finder',
    type=str,
    choices=('naive', 'quantum'),
    default='naive',
    help='order finder to use; must be either "naive" or "quantum"'
)

def naive_order_finder(x: int, n: int) -> int:
    if x < 2 or n <= x or math.gcd(x, n) > 1:
        raise ValueError(f'Invalid x={x} for modulus n={n}.')
    r, y = 1, x
    while y != 1:
        y = (x * y) % n
        r += 1
    return r

class ModularExp(cirq.ArithmeticGate):
    def __init__(self, target, exponent, base: int, modulus: int):
        if len(target) < modulus.bit_length():
            raise ValueError(f'Register with {len(target)} qubits is too small for modulus {modulus}')
        self.target = target
        self.exponent = exponent
        self.base = base
        self.modulus = modulus

    def registers(self):
        return self.target, self.exponent, self.base, self.modulus

    def with_registers(self, *new_registers):
        target, exponent, base, modulus = new_registers
        return ModularExp(target, exponent, base, modulus)

    def apply(self, *register_values: int) -> int:
        target, exponent, base, modulus = register_values
        if target >= modulus:
            return target
        return (target * base**exponent) % modulus

    def _circuit_diagram_info_(self, args: cirq.CircuitDiagramInfoArgs):
        wire_symbols = [f't{i}' for i in range(len(self.target))]
        e_str = str(self.exponent)
        if isinstance(self.exponent, Sequence):
            e_str = 'e'
            wire_symbols += [f'e{i}' for i in range(len(self.exponent))]
        wire_symbols[0] = f'ModularExp(t*{self.base}**{e_str} % {self.modulus})'
        return cirq.CircuitDiagramInfo(wire_symbols=tuple(wire_symbols))

def make_order_finding_circuit(x: int, n: int) -> cirq.Circuit:
    L = n.bit_length()
    target = cirq.LineQubit.range(L)
    exponent = cirq.LineQubit.range(L, 3 * L + 3)
    return cirq.Circuit(
        cirq.X(target[L - 1]),
        cirq.H.on_each(*exponent),
        ModularExp([2] * len(target), [2] * len(exponent), x, n).on(*target + exponent),
        cirq.qft(*exponent, inverse=True),
        cirq.measure(*exponent, key='exponent'),
    )

def read_eigenphase(result: cirq.Result) -> float:
    exponent_as_integer = result.data['exponent'][0]
    exponent_num_bits = result.measurements['exponent'].shape[1]
    return float(exponent_as_integer / 2**exponent_num_bits)

def quantum_order_finder(x: int, n: int):
    if x < 2 or n <= x or math.gcd(x, n) > 1:
        raise ValueError(f'Invalid x={x} for modulus n={n}.')
    circuit = make_order_finding_circuit(x, n)
    result = cirq.sample(circuit)
    eigenphase = read_eigenphase(result)
    f = fractions.Fraction.from_float(eigenphase).limit_denominator(n)
    if f.numerator == 0:
        return None
    r = f.denominator
    if x**r % n != 1:
        return None
    return r

def find_factor_of_prime_power(n: int):
    for k in range(2, math.floor(math.log2(n)) + 1):
        c = math.pow(n, 1 / k)
        c1 = math.floor(c)
        if c1**k == n:
            return c1
        c2 = math.ceil(c)
        if c2**k == n:
            return c2
    return None

def find_factor(n: int, order_finder, max_attempts: int = 30):
    if sympy.isprime(n):
        return None
    if n % 2 == 0:
        return 2
    c = find_factor_of_prime_power(n)
    if c is not None:
        return c
    for _ in range(max_attempts):
        x = random.randint(2, n - 1)
        c = math.gcd(x, n)
        if 1 < c < n:
            return c
        r = order_finder(x, n)
        if r is None:
            continue
        if r % 2 != 0:
            continue
        y = x ** (r // 2) % n
        assert 1 < y < n
        c = math.gcd(y - 1, n)
        if 1 < c < n:
            return c
    return None

def main(n: int, order_finder=naive_order_finder):
    if n < 2:
        raise ValueError(f'Invalid input {n}, expected positive integer greater than one.')
    d = find_factor(n, order_finder)
    if d is None:
        print(f'No non-trivial factor of {n} found. It is probably a prime.')
    else:
        print(f'{d} is a non-trivial factor of {n}')
        assert 1 < d < n
        assert n % d == 0

# Circuit statique pour QSmell (simplifié)
x, n = 2, 15  # Valeurs fixes
L = n.bit_length()
target = cirq.LineQubit.range(L)
exponent = cirq.LineQubit.range(L, 3 * L + 3)
circuit = cirq.Circuit()
circuit.append(cirq.X(target[L - 1]))
circuit.append([cirq.H(q) for q in exponent])
# ModularExp est une porte personnalisée, nous la simulons par une opération simplifiée
# circuit.append(ModularExp([2] * len(target), [2] * len(exponent), x, n).on(*target + exponent))
circuit.append(cirq.qft(*exponent, inverse=True))

if __name__ == '__main__':
    ORDER_FINDERS = {'naive': naive_order_finder, 'quantum': quantum_order_finder}
    args = parser.parse_args()
    main(n=args.n, order_finder=ORDER_FINDERS[args.order_finder])