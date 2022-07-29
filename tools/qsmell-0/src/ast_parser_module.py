import ast
import re
from collections import defaultdict
from base_util import *
from helper import *
from is_comment_module import is_comment


def extract_pure_function_name_from_function_signature(function_definition: str) -> str:
    """
    Extract pure function name from a def function signature
    :param function_definition: def hi():
    :return: hi
    """
    function_definition = function_definition.strip()
    split_list = function_definition.split(" ")
    if function_definition.count(" ") == 1:
        x = split_list[1].split("(")[0]
        if len(x) > 0 and x[-1] == ")":
            return x[:-1]
        return x
    x = function_definition.split("(")[0].split(" ")[-1]
    if len(x) > 0 and x[-1] == ")":
        return x[:-1]
    return x


def extract_pure_class_name_from_class_signature(class_definition: str) -> str:
    """
    Extract class name from a class definition signature
    :param class_definition: class h(k): or class h
    :return: h
    """
    class_line = class_definition.split("\n")[0]
    if '(' not in class_line:
        if class_line[-1] == ':':
            return class_line.split(' ')[1].strip()[:-1]
        else:
            return class_line.split(' ')[1].strip()
    else:
        return class_line.split(' ')[1].split('(')[0].strip()


class MyNodeVisitor(ast.NodeVisitor):
    def __init__(self, source):
        self.source = source
        self.class_dict = defaultdict(str)
        self.function_dict = defaultdict(str)

    def visit_FunctionDef(self, node):
        function_definition = ast.get_source_segment(self.source, node)
        function_name = extract_pure_function_name_from_function_signature(function_definition)
        self.function_dict[function_name] = function_definition

    def visit_ClassDef(self, node):
        class_definition = ast.get_source_segment(self.source, node)
        class_name = extract_pure_class_name_from_class_signature(class_definition)
        self.class_dict[class_name] = class_definition

    def get_all_dicts(self):
        return self.class_dict, self.function_dict


def find_class_start_line_number(class_name, file_dir):
    target_line = "class {}".format(class_name)
    with open(file_dir, 'r') as f:
        full_content = f.readlines()
    for line_count, line in enumerate(full_content):
        if target_line in line:
            return line_count


def find_function_start_line_number(function_name, file_dir):
    with open(file_dir, 'r') as f:
        full_content = f.readlines()
    target_line = "def " + function_name
    for line_count, line in enumerate(full_content):
        if target_line in line:
            return line_count


def build_parameter_infectious_list(parameter, function_implementation_list, function_name):
    result_list = list()
    if '=' in parameter:
        parameter = parameter.split('=')[0].strip()
    infectious_list = [parameter]
    for line, line_count in function_implementation_list:
        if '=' not in line or '==' in line:
            continue
        left_list = line.strip().split("=", 1)[0].strip()
        right_expr = line.strip().split('=', 1)[1].strip()
        if '(' in right_expr:
            current_parameter_list = build_statement_call_parameter_list(line)
            if 'None' in current_parameter_list:
                current_parameter_list.remove('None')
            if parameter in current_parameter_list:
                for affected_term in left_list.split(','):
                    result_list.append((parameter, affected_term, "function", function_name))
                    infectious_list.append(affected_term)
        else:
            tokenize_list = re.split("\W+", right_expr)
            for token in tokenize_list:
                token = token.split("(", 1)[0]
                token = token.split('[', 1)[0]
                if token.strip() in infectious_list:
                    for affected_term in left_list.split(','):
                        result_list.append((parameter, affected_term, "function", function_name))
                        infectious_list.append(affected_term)
    return result_list


class MyAstParser:
    def __init__(self, file_dir):
        self.file_content = read_file(file_dir)
        self.file_dir = file_dir
        self.class_dict = defaultdict(lambda: defaultdict(list))
        self.function_implementation_dict = defaultdict(list)
        self.line_info_dict = defaultdict(tuple)
        self.global_full_statement_list = list()
        self.function_parameter_variable_associate_dict = defaultdict(list)

    def refine_class_dict(self, class_dict):
        """ Changes from function_imp str to function statement list """
        for class_name in class_dict:
            class_start_line_number = find_class_start_line_number(class_name, self.file_dir)
            class_definition_list = class_dict[class_name].split('\n')
            class_definition_line = class_definition_list[0]
            method_line_dict = defaultdict(list)
            method_pure_name = None
            for line_count, line in enumerate(class_definition_list[1:], class_start_line_number + 1):
                if "def " in line.strip():
                    method_pure_name = extract_pure_function_name_from_function_signature(line)
                if method_pure_name is not None:
                    method_line_dict[method_pure_name].append((line, line_count))
            self.class_dict[(class_name, class_definition_line, class_start_line_number)] = method_line_dict

    def refine_function_implementation_dict(self, function_implementation_dict):
        """ This function reformat the function implementation dict from str to list """
        for function_name in function_implementation_dict:
            function_start_line_number = find_function_start_line_number(function_name, self.file_dir)
            for line_num, line in enumerate(function_implementation_dict[function_name].split('\n'),
                                            function_start_line_number):
                line = line.strip()
                self.function_implementation_dict[function_name].append((line, line_num))

    def build_line_info_dict(self):
        with open(self.file_dir, 'r') as f:
            full_content = f.readlines()
        line_count = 0
        while line_count < len(full_content):
            line = full_content[line_count].strip()

            if 'import ' in line or 'from ' in line:
                self.line_info_dict[(line, 'global', "import")] = (line_count, line_count)
                line_count += 1
                continue
            elif 'def ' in line:
                function_name = extract_pure_function_name_from_function_signature(line)
                length = len(self.function_implementation_dict[function_name])
                self.line_info_dict[(line, 'function', function_name)] = (line_count, line_count + length - 1)
                line_count += length
                continue
            elif 'class ' in line:
                class_name = extract_pure_class_name_from_class_signature(line)
                class_implementation_dict = self.class_dict[(class_name, line, line_count)]
                length = 0
                for method_name in class_implementation_dict:
                    length += len(class_implementation_dict[method_name])
                length += 1  # + 1 for class definition line
                self.line_info_dict[(line, 'class', class_name)] = (line_count, line_count + length - 1)
                line_count += length
                continue
            else:
                self.line_info_dict[(line, 'global', "None")] = (line_count, line_count)
                line_count += 1
                continue

    def build_global_full_statement_list(self):
        """ This function builds a list of all global full statements """
        with open(self.file_dir, 'r') as f:
            full_content = f.readlines()
        for line, scope, name in self.line_info_dict:
            if scope == 'global' and name == 'None':
                line_number = self.line_info_dict[(line, scope, name)][0]
                if is_comment(line, line_number, full_content):
                    continue
                self.global_full_statement_list.append((line, line_number))

    def refine_results(self, class_dict, function_implementation_dict):
        self.refine_class_dict(class_dict)
        self.refine_function_implementation_dict(function_implementation_dict)
        self.build_line_info_dict()
        self.build_global_full_statement_list()

    def build_function_parameter_variable_associate_dict(self):
        for function_name in self.function_implementation_dict:
            function_implementation_detail_list = self.function_implementation_dict[function_name]
            function_signature, function_signature_line_number = function_implementation_detail_list[0]
            function_implementation_detail_list = function_implementation_detail_list[1:]
            call_parameter_name_list = function_signature.split("def ", 1)[1].strip().split("(", 1)[1].strip()[:-2].split(',')
            call_parameter_name_list = list(filter(lambda x: (x.strip() != ""), call_parameter_name_list))
            function_all_list = list()
            for parameter in call_parameter_name_list:
                parameter = parameter.strip()
                parameter_infectious_list = build_parameter_infectious_list(parameter, function_implementation_detail_list, function_name)
                print("for parameter: ", parameter, " parameter infectious list = ", parameter_infectious_list)
                function_all_list += parameter_infectious_list
            self.function_parameter_variable_associate_dict[function_name] = function_all_list

    def parse_file(self):
        try:
            tree = ast.parse(self.file_content)
            visitor = MyNodeVisitor(self.file_content)
            visitor.visit(tree)
            class_dict, function_implementation_dict = visitor.get_all_dicts()
        except Exception:
            class_dict = dict()
            function_implementation_dict = dict()
        self.refine_results(class_dict, function_implementation_dict)
        self.build_function_parameter_variable_associate_dict()

    def get_class_dict(self):
        return dict(self.class_dict)

    def get_function_implementation_dict(self):
        return dict(self.function_implementation_dict)

    def get_global_full_statement_list(self):
        return self.global_full_statement_list

    def get_line_info_dict(self):
        return dict(self.line_info_dict)

    def get_file_dir(self):
        return self.file_dir

    def get_function_parameter_variable_associate_dict(self):
        return self.function_parameter_variable_associate_dict