import re
from ast_parser_module import *


def analysis_register_statement(line, file_line_list, line_count):
    statement = line.split('=', 1)[1].strip()
    parameters = statement.split('(', 1)[1][:-1].strip()
    bit_name = ""
    num_bits_variable_name = ""
    num_bits = ""
    for parameter in parameters.split(','):
        word_tokens = parameter.split('=')
        word_tokens = [x.strip() for x in word_tokens]
        if ('name=' in word_tokens) or ('name' in word_tokens):
            bit_name = parameter.split("=")[1].strip()
        elif parameter.isnumeric():
            num_bits = int(parameter)
        else:
            num_bits_variable_name = parameter.strip()
    partial_content = file_line_list[:line_count]
    partial_content.reverse()
    for line_number in range(len(partial_content)):
        line = partial_content[line_number].strip()
        if is_comment(line, line_number + line_count - 1, file_line_list) or line == "" or line.startswith("##") or '=' not in line:
            continue
        variable, statement = line.split("=", 1)
        statement = statement.split('#')[0].strip()
        if variable.strip() == num_bits_variable_name and statement.strip().isdigit():
            num_bits = int(statement.strip())
    return num_bits, bit_name


class MyCircuitBitParser:
    def __init__(self, my_parsed_object):
        self.file_dir = my_parsed_object.get_file_dir()
        self.line_info_dict = my_parsed_object.get_line_info_dict()
        self.function_implementation_dict = my_parsed_object.get_function_implementation_dict()
        self.global_full_statement_list = my_parsed_object.get_global_full_statement_list()

        self.global_bit_list = list()
        self.file_defined_bit_list = list()
        self.global_circuit_list = list()
        self.file_defined_circuit_list = list()
        self.file_infectious_bit_name_list = list()  # x = QuantumRegister(), y = x, so [y]
        self.file_infectious_circuit_name_list = list()

    def build_global_scope_bit_circuit_collections(self):
        for bit_name, scope, name in self.file_defined_bit_list:
            if scope == 'global':
                self.global_bit_list.append((bit_name, scope, name))

        for circuit_name, scope, name in self.file_defined_circuit_list:
            if scope == 'global':
                self.global_circuit_list.append((circuit_name, scope, name))

    def find_contained_bit_name(self, token, current_scope_name):
        for bit_name, scope, name in self.file_defined_bit_list:
            if bit_name == token and scope == 'global':
                return True, bit_name
            if bit_name == token and scope == 'function' and name == current_scope_name:
                return True, bit_name
        return False, None

    def find_contained_circuit_name(self, token, current_scope_name):
        for circuit_name, scope, name in self.file_defined_circuit_list:
            if circuit_name == token and scope == 'global':
                return True, circuit_name
            if circuit_name == token and scope == 'function' and name == current_scope_name:
                return True, circuit_name
        return False, None

    def build_file_infectious_bit_list(self):
        for function_name in self.function_implementation_dict:
            function_implementation_line_number_list = self.function_implementation_dict[function_name]
            for function_implementation_line, line_number in function_implementation_line_number_list:
                function_implementation_line = function_implementation_line.strip()
                if '=' not in function_implementation_line or 'QuantumRegister(' in function_implementation_line:
                    continue
                left, right = get_left_right(function_implementation_line)
                tokenize_list = re.split("\W+", right)
                for token in tokenize_list:
                    if '[' in token and not token.startswith('['):
                        token = token.split("[", 1)[0].strip()
                    is_contained_bit_name_result, contained_bit_name = self.find_contained_bit_name(token, function_name)
                    if not is_contained_bit_name_result:
                        continue
                    self.file_infectious_bit_name_list.append((contained_bit_name, left, 'function', function_name))

    def build_file_infectious_circuit_list(self):
        for function_name in self.function_implementation_dict:
            function_implementation_line_number_list = self.function_implementation_dict[function_name]
            for function_implementation_line, line_number in function_implementation_line_number_list:
                function_implementation_line = function_implementation_line.strip()
                if '=' not in function_implementation_line or 'QuantumCircuit(' in function_implementation_line:
                    continue
                left, right = get_left_right(function_implementation_line)
                tokenize_list = re.split("\W+", right)
                for token in tokenize_list:
                    if '[' in token and not token.startswith('['):
                        token = token.split("[", 1)[0].strip()
                    is_contained_circuit_name_result, contained_circuit_name = self.find_contained_circuit_name(token, function_name)
                    if not is_contained_circuit_name_result:
                        continue
                    self.file_infectious_circuit_name_list.append((contained_circuit_name, left, 'function', function_name))

    def build_all_lists(self, file_line_list):
        for line_count, line in enumerate(file_line_list):
            line = line.strip()
            scope, name = find_line_scope(line_count, self.line_info_dict)
            variable, statement = get_left_right(line)
            if 'QuantumRegister(' in line:
                num_bits, bit_name = analysis_register_statement(line, file_line_list, line_count)
                if variable is not None:
                    bit_name = variable
                bit_name = bit_name.replace('"', "")
                bit_name = bit_name.replace("'", '')
                self.file_defined_bit_list.append((bit_name, scope, name))
            elif 'QuantumCircuit(' in line:
                circuit_name = line.split('=', 1)[0].strip()
                self.file_defined_circuit_list.append((circuit_name, scope, name))
        self.build_global_scope_bit_circuit_collections()
        self.build_file_infectious_bit_list()
        self.build_file_infectious_circuit_list()

    def parse_file(self):
        with open(self.file_dir, 'r') as f:
            file_line_list = f.readlines()
        self.build_all_lists(file_line_list)

    def get_global_bit_list(self):
        return self.global_bit_list

    def get_file_defined_bit_list(self):
        return self.file_defined_bit_list

    def get_global_circuit_list(self):
        return self.global_circuit_list

    def get_file_defined_circuit_list(self):
        return self.file_defined_circuit_list

    def get_file_infectious_bit_name_list(self):
        return self.file_infectious_bit_name_list

    def get_file_infectious_circuit_name_list(self):
        return self.file_infectious_circuit_name_list
