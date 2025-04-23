""" Lack of physical qubit (LPQ) """

import sys
import pandas as pd
import ast
import cirq
from .ISmell import *

class LPQ(ISmell):

    def __init__(self):
        super().__init__("LPQ")

    def compute_metric_ast(self, tree: ast.AST, output_file_path: str) -> None:
        metrics = {
            'metric': self._name,
            'value': 1  # Par défaut, aucun dispositif
        }

        class DeviceVisitor(ast.NodeVisitor):
            def visit_Import(self, node):
                for alias in node.names:
                    if alias.name == 'cirq':
                        self.cirq_imported = True
            def visit_Name(self, node):
                if getattr(self, 'cirq_imported', False) and node.id == 'Device':
                    metrics['value'] = 0  # Dispositif trouvé

        DeviceVisitor().visit(tree)

        out_df = pd.DataFrame.from_dict([metrics])
        sys.stdout.write(str(out_df) + '\n')
        out_df.to_csv(output_file_path, header=True, index=False, mode='w')