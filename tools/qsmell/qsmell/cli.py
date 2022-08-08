""" Command Line Interface Module. """

import argparse
import os
import pathlib

from qsmell import QSmell
from .smell import SmellType

def main():
    dir = os.path.dirname(os.path.abspath(__file__))
    version = {}
    with open(os.path.join(dir, "version.py")) as fp:
        exec(fp.read(), version)

    cli = CLI(version['__version__'])
    cli.config()
    cli.run()

class CLI:
    """ Class for wrapping the CLI interface.
    
    Attributes:
        args: command line arguments
        version: qsmell version
    """
    def __init__(self, version):
        self.args = None
        self.version = version
        self.config()

    def config(self):
        parser = argparse.ArgumentParser(description='Detects quantum-based code smells in programs with in the Qiskit framework.')
        parser.add_argument('--version', '-v', action='version', version='%(prog)s {}'.format(self.version))
        parser.add_argument('--smell-metric', '-s', help="Quantum smell metric to compute", required=False, type=SmellType.argparse, choices=list(SmellType), default=SmellType.CG)
        parser.add_argument('--input-file', '-i', action='store', help="Quantum program/circuit to analyse", required=True, type=pathlib.Path)
        parser.add_argument('--output-file', '-o', action='store', help="Output file", required=True, type=pathlib.Path)
        self.args = parser.parse_args()

    def run(self):
        smell: ISmell    = self.args.smell_metric.value
        input_file: str  = self.args.input_file.as_posix()
        output_file: str = self.args.output_file.as_posix()
        qsmell = QSmell()
        qsmell.run(smell, input_file, output_file)
