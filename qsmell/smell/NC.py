""" Non-parameterized circuit (NC) """

import sys
import ast
import pandas as pd
import cirq
from .ISmell import *

class NC(ISmell):

    def __init__(self):
        super().__init__("NC")

    def compute_metric(self, circuit_or_df: cirq.Circuit | pd.DataFrame, output_file_path: str) -> None:
        metrics = {
            'metric': self._name,
            'value': 0
        }

        if isinstance(circuit_or_df, cirq.Circuit):
            # Vérifier si le circuit utilise des paramètres
            has_params = any(
                isinstance(p, (sympy.Symbol, cirq.ParameterizedValue))
                for op in circuit_or_df.all_operations()
                for p in getattr(op.gate, 'parameters', [])
            )
            metrics['value'] = 0 if has_params else 1

        elif isinstance(circuit_or_df, pd.DataFrame):
            metrics['value'] = 1  # Par défaut, assume non paramétrisé pour DataFrame

        out_df = pd.DataFrame.from_dict([metrics])
        sys.stdout.write(str(out_df) + '\n')
        out_df.to_csv(output_file_path, header=True, index=False, mode='w')

    def compute_metric_ast(self, tree: ast.Module, output_file_path: str) -> None:
        loops_lines = []
        for node in ast.walk(tree):
            if isinstance(node, ast.For) or isinstance(node, ast.While):
                loop_start = node.lineno
                loop_end = node.body[-1].lineno
                loops_lines.extend(range(loop_start, loop_end + 1))

        num_executions = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute):
                    if func.attr == 'run' and isinstance(func.value, ast.Name) and func.value.id == 'cirq':
                        print(f'  Found a run call at line {node.lineno}')
                        num_executions += 1
                        if node.lineno in loops_lines:
                            num_executions += 1  # Suppose exécution multiple dans une boucle

            elif isinstance(node, ast.Expr):
                value = node.value
                if isinstance(value, ast.Call):
                    func = value.func
                    if isinstance(func, ast.Attribute):
                        if func.attr == 'run' and isinstance(func.value, ast.Name) and func.value.id == 'cirq':
                            print(f'  Found an expression run call at line {node.lineno}')
                            num_executions += 1
                            if node.lineno in loops_lines:
                                num_executions += 1

        num_bind_parameters = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute):
                    if func.attr == 'with_parameters' and isinstance(func.value, ast.Name) and func.value.id == 'circuit':
                        print(f'  Found a parameter binding at line {node.lineno}')
                        num_bind_parameters += 1

        value = max(0, num_executions - num_bind_parameters)

        metrics = {
            'metric': self._name,
            'value': value
        }

        out_df = pd.DataFrame.from_dict([metrics])
        sys.stdout.write(str(out_df) + '\n')
        out_df.to_csv(output_file_path, header=True, index=False, mode='w')