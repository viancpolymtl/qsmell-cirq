# QSmell

QSmell is a tool for detecting quantum-based code smells in programs written in the [Qiskit framework](https://qiskit.org).  As Qiskit v0.37.0 requires Python version >= v3.7.8, QSmell requires Python v3.7.8 as well.

## Workflow

Depending on the smell metric, QSmell either performs a dynamic or static analysis.

The smell metrics CG, ROC, LC, IM, IdQ, and IQ that rely on an accurate data as the set of qubits and/or the set of operations performed in the circuit, are computed using a dynamic analysis.  The other smell metrics, NC and LPQ, which do not rely on the quantum circuit but the actions performed on the quantum circuit, are computed using a static analysis.  The latter does not handle common code as loops or to track objects passed as arguments to other functions, thus it is possible evaluate it with a static analysis.  The former does not handle calls to methods that are not part of a quantum circuit object (e.g., `transpile`, Qiskit backends' methods), thus it is necessary to analyse it dynamically.

### Dynamic Analysis

To perform a dynamic analysis on a quantum program, QSmell takes as input an **execution matrix**, whereas each row represents a quantum or classical bit, each column represents a timestamp in the circuit, and each cell represents a quantum operation performed in the circuit.

Given the following running example (`example.py`)

```python
# example.py
from qiskit import QuantumCircuit, QuantumRegister, Aer

reg = QuantumRegister(3, name='reg')
qc = QuantumCircuit(reg)
qc.x(reg[0])
for i in range(0, 2):
    qc.x(reg[i])
qc.x(reg[1])
qc.x(reg[0])
qc.x(reg[2])
qc.y(reg[1])

backend = Aer.get_backend('qasm_simulator')
qc = transpile(qc, backend, initial_layout=[3, 4, 2])
job = backend.run(qc)
```

one would have to manually inject the following piece code

```python
from quantum_circuit_to_matrix import qc2matrix
qc2matrix(qc, output_file_path='example-matrix.csv')
```

adapt it, in case, e.g., the quantum circuit may not be named `qc`, and run it to generate the **execution matrix**.  Note that the `quantum_circuit_to_matrix` module was built by us on top of Qiskit's API and is part of the QSmell distribution.

For this running example the **execution matrix** is

```
             1 &   2 &   3
q-reg-0} & x() & x() & x()
q-reg-1} & x() & x() & y()
q-reg-2} & x() & x() &    
```

This manual step could not, at the time of writing this document, be automatized as different programs could be coded differently.  For example, although `qc` is a standard name of the variable that holds a `QuantumCircuit` object, it might have been namely differently or it might be under a method of the program itself.  For example, to get the `QuantumCircuit` object of the [`vqd` program](https://github.com/Qiskit/qiskit-terra/blob/0.21.0/qiskit/algorithms/eigen_solvers/vqd.py), one would have to invoke the [`construct_circuit` method](https://github.com/Qiskit/qiskit-terra/blob/0.21.0/qiskit/algorithms/eigen_solvers/vqd.py#L408) of the `vqd` class to retrieve its `QuantumCircuit` object.

Once the **execution matrix** has been generated, to compute, e.g., the LC smell metric, QSmell first computes the maximum number of operations in any qubit (any row in the matrix).   In above example, such maximum is three in qubit `q-reg-0`, for example.  It then performs a similar procedure to compute the maximum number of operations that are performed simultaneous (i.e., in the same timestamp/column).  The maximum number of operations (i.e., three) are performed in the first and second column.  Finally, the LC metric is (1 - 0.03512)^{3 * 3} = 0.725.

### Static Analysis

As the information of the quantum backend (see lines 14-16 of the running example) is not kept in the quantum circuit object itself, QSmell performs a static analysis for smell metrics NC and LPQ.  It takes a source code `.py` file and analysis it using [Python AST](https://docs.python.org/3.7/library/ast.html).  To compute the LPQ smell metric for the running example, QSmell first finds all calls to the `transpile` method in the program's under analysis AST and then counts how many do not define the `initial_layout` parameter.

## Installation

Installing and using QSmell is simple and straightforward.  First, one should get its latest version from [pip](https://pypi.org).

```
pip install qsmell # Not yet deployed for anonymity
```

or from the tool's repository:

```
git clone <URL redacted for anonymity>
```

and compile/install QSmell from it's source code

```
python3 setup.py install
```

## Usage example

Given the following quantum program (`example.py`)

```python
# example.py
from qiskit import QuantumCircuit, QuantumRegister, Aer

reg = QuantumRegister(3, name='reg')
qc = QuantumCircuit(reg)
qc.x(reg[0])
for i in range(0, 2):
    qc.x(reg[i])
qc.x(reg[1])
qc.x(reg[0])
qc.x(reg[2])
qc.y(reg[1])

backend = Aer.get_backend('qasm_simulator')
qc = transpile(qc, backend, initial_layout=[3, 4, 2])
job = backend.run(qc)
```

one could run QSmell as

```
qsmell \
  --smell-metric "ROC" \
  --input-file "example-matrix.csv" \
  --output-file "roc-smell-metric.csv"
```

which produces the following CSV file:

```
metric,value
ROC,2
```

To perform static analysis, or in other words, to compute the NC or LQP smell metrics one could invoke QSmell on the source code under analysis as:

```
qsmell \
  --smell-metric "NC" \
  --input-file "example.py" \
  --output-file "nc-smell-metric.csv"
```

### Command-line arguments

```
  -h, --help            show this help message and exit
  --version, -v         show program's version number and exit
  --smell-metric {CG,ROC,NC,LC,IM,IdQ,IQ,AQ,LPQ}, -s {CG,ROC,NC,LC,IM,IdQ,IQ,AQ,LPQ} Quantum smell metric to compute
  --input-file INPUT_FILE, -i INPUT_FILE Quantum program/circuit to analyse
  --output-file OUTPUT_FILE, -o OUTPUT_FILE Output file
```
