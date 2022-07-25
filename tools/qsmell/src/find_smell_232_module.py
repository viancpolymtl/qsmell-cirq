from collections import defaultdict
from base_util import *
from helper import *


def is_measured_circuit_object(method_call_object_name, circuit_list):
    for circuit_name, scope, name in circuit_list:
        if circuit_name == method_call_object_name:
            return True


def is_empty_measurement(first_measure_dict):
    for quantum_name in first_measure_dict:
        return False
    return True


def is_new_circuit_assignment(statement_token_list, file_defined_circuit_name_list, file_infectious_circuit_name_list, new_added_circuit_name_list):
    for token in statement_token_list:
        if token in file_infectious_circuit_name_list or token in file_defined_circuit_name_list:
            return True
        if token in new_added_circuit_name_list:
            return True
    return False


def is_file_defined_circuit_name(object_call_name, file_defined_circuit_name_list):
    for circuit_name, scope, name in file_defined_circuit_name_list:
        if circuit_name == object_call_name:
            return True
    return False


def is_infectious_circuit_name(object_call_name, file_infectious_circuit_name_list):
    for circuit_source_name, circuit_destination_name, scope, name in file_infectious_circuit_name_list:
        if circuit_source_name == object_call_name and circuit_destination_name == object_call_name:
            return True
    return False


def get_statement_token_list(statement):
    """ This function takes a statement, return a list of tokens depending on the type of statement """
    # if it is a non call statement i.e. x = fly + 3
    # return [fly, 3]
    # if it is a call statement i.e. x = hello(fly, v)
    # return [fly, v]
    # if it is a mix like x = y + hello(fly, v)
    # return [y, fly, v]
    result_list = []
    if '(' not in statement:
        y = re.split(r"\]", statement)
        z = []
        for i in y:
            i = i.strip()
            if '[' in i:
                z.append(i + ']')
            else:
                z.append(i)
        for x in z:
            x = x.split('+', 1)[0].strip()
            x = x.split('-', 1)[0].strip()
            x = x.split('*', 1)[0].strip()
            x = x.split('/', 1)[0].strip()
            x = x.split('//', 1)[0].strip()
            x = x.split('**', 1)[0].strip()
            x = x.strip()
            if x == "":
                continue
            result_list.append(x)
    else:
        result_list = statement.split("(",1)[1].strip().split(")",1)[0].strip().split(',')
        result_list = list(filter(lambda x: (x.strip() != ""), result_list))
        result_list = list(map(lambda x: (x.strip()), result_list))

    return result_list


def is_target_circuit_object(method_call_object_name, file_defined_circuit_name_list, file_infectious_circuit_name_list):
    if is_file_defined_circuit_name(method_call_object_name, file_defined_circuit_name_list):
        return True
    if is_infectious_circuit_name(method_call_object_name, file_infectious_circuit_name_list):
        return True


def build_first_measure_dict(file_defined_circuit_name_list, call_order_line_list, file_infectious_circuit_name_list, line_info_dict):
    first_measure_dict = defaultdict(tuple)
    new_added_circuit_name_list = list()
    for line_statement, line_number in call_order_line_list:
        variable, statement = get_left_right(line_statement.strip())
        statement_token_list = get_statement_token_list(statement)
        scope, name = find_line_scope(line_number, line_info_dict)
        if is_call_statement(statement) and 'def ' not in statement:
            method_call_object_name, function_call_pure_name = analysis_call_statement(statement)
            if function_call_pure_name == 'measure' and is_target_circuit_object(method_call_object_name, file_defined_circuit_name_list, file_infectious_circuit_name_list):
                first_measure_dict[method_call_object_name] = (line_statement, line_number)
        else:  # 是普通statement包括for, while loop
            if not is_new_circuit_assignment(statement_token_list, file_defined_circuit_name_list, file_infectious_circuit_name_list, new_added_circuit_name_list):
                continue
            if variable is not None:
                new_added_circuit_name_list.append((variable, scope, name))
    return first_measure_dict


def find_smell_232(my_parsed_object, my_circuit_bit_object, call_order_line_list):
    file_defined_circuit_name_list = my_circuit_bit_object.get_file_defined_circuit_list()
    line_info_dict = my_parsed_object.get_line_info_dict()
    file_infectious_circuit_name_list = my_circuit_bit_object.get_file_infectious_circuit_name_list()
    first_measure_dict = build_first_measure_dict(file_defined_circuit_name_list, call_order_line_list,
                                                  file_infectious_circuit_name_list, line_info_dict)
    if is_empty_measurement(first_measure_dict):
        return False
    for circuit_name in first_measure_dict:
        first_measure_statement, first_measure_line_number = first_measure_dict[circuit_name]
        first_statement_index = call_order_line_list.index((first_measure_statement, first_measure_line_number))
        partial_call_order_line_list = call_order_line_list[first_statement_index + 1:]
        for partial_statement, partial_line_num in partial_call_order_line_list:
            if '(' not in partial_statement or '.' not in partial_statement:
                continue
            method_call_object_name = partial_statement.split(".", 1)[0].strip()
            method_name = partial_statement.split('.', 1)[1].strip().split("(", 1)[0].strip()
            if method_name == 'draw':
                continue
            if is_measured_circuit_object(method_call_object_name, file_defined_circuit_name_list):
                return True
    return False
