# QSmell

QSmell is a tool for detecting quantum-based code smells in programs written in the [Qiskit framework](https://qiskit.org).  QSmell supports Python ??.? and Qiskit ??.? and given a quantum circuit as a coverage matrix, it generates a smell report of the circuit.

## Installation

You can easily install QSmell from sources:

```
$ python3 setup.py install
```

## Usage example

```
mkdir -p "../../experiments/data/generated/CG"

python3 -m qsmell \
  --smell-metric CG \
  --input-file ../../subjects/data/generated/quantum-circuit-as-matrix/ch04_02_teleport_fly.csv \
  --output-file ../../experiments/data/generated/CG/ch04_02_teleport_fly.csv
```

### Command-line arguments

```
  -h, --help            show this help message and exit
  --version, -v         show program's version number and exit
  --smell-metric {CG,ROC,NC,LC,IM,IdQ,IQ,AQ,LPQ}, -s {CG,ROC,NC,LC,IM,IdQ,IQ,AQ,LPQ} Quantum smell metric to compute
  --input-file INPUT_FILE, -i INPUT_FILE Quantum circuit to analyse as a matrix
  --output-file OUTPUT_FILE, -o OUTPUT_FILE Output file
```
