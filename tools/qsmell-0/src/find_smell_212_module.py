from ast_parser_module import *
from base_util import *
from helper import *


def initial_check(file_dir):
    """ This function checks if contains QuantumCircuit and QuantumRegister"""
    circuit_imported = False
    register_imported = False
    with open(file_dir, 'r') as f:
        file_list = f.readlines()
    for line in file_list:
        if 'QuantumCircuit' in line:
            circuit_imported = True
        if 'QuantumRegister' in line:
            register_imported = True
        if circuit_imported and register_imported:
            return True
    return False


def is_contain_global_call_source_variable(partial_call_order_line_list, method_call_object_name, line_scope_name, parameter_index, my_parsed_object, my_circuit_bit_object):
    partial_call_order_line_list.reverse()
    target_call_str = line_scope_name + '('
    for visiting_statement, visiting_line_number in partial_call_order_line_list:
        if target_call_str not in visiting_statement or visiting_statement.startswith("def "):
            continue
        visiting_statement_parameter_list = build_statement_call_parameter_list(visiting_statement)
        visiting_statement_target_parameter = find_visiting_statement_target_parameter(visiting_statement_parameter_list, parameter_index, line_scope_name, my_parsed_object, method_call_object_name)
        if visiting_statement_target_parameter == method_call_object_name:
            return True
        elif convert_infectious_to_source(visiting_statement_target_parameter,my_circuit_bit_object.get_file_infectious_bit_name_list()) == method_call_object_name:
            return True
        current_statement_scope, current_line_scope_name = find_line_scope(visiting_line_number, my_parsed_object.get_line_info_dict())
        ''' Below for variable that needs to be check previously.'''
        if current_statement_scope == 'function':
            target_call_str = current_line_scope_name + '('
            associated_parameter_name = extract_associated_parameter_name(my_parsed_object.get_function_parameter_variable_associate_dict(), visiting_statement_target_parameter, current_line_scope_name)
            if associated_parameter_name is None:
                associated_parameter_name = visiting_statement_target_parameter
            if associated_parameter_name.startswith('(') or associated_parameter_name.startswith("["):
                associated_parameter_name = associated_parameter_name[1:]
                associated_parameter_name = associated_parameter_name.split('[', 1)[0].strip()
                associated_parameter_name = associated_parameter_name.split('(', 1)[0].strip()
            associated_parameter_index = find_associated_parameter_index(associated_parameter_name, my_parsed_object.get_function_implementation_dict(),
                                                                         current_line_scope_name, visiting_statement)
            if associated_parameter_index is None:
                return False
        elif current_statement_scope == 'global':
            if is_contain_circuit_name(my_circuit_bit_object, visiting_statement_target_parameter, current_statement_scope, current_line_scope_name):
                return True
    return False


def filter_circuit_call_list(circuit_call_list):
    result_list = list()
    for line, line_number in circuit_call_list:
        if '.barrier(' in line:
            continue
        result_list.append((line, line_number))
    return result_list


def filter_non_customized_gate(exclude_barrier_circuit_call_list):
    """ This function reads a white list and remove official one """
    white_list_dir = "/Users/qihongchen/Desktop/quantum_smell_project/resources/Built-in-Qiskit-Gates.txt"
    white_list = list()
    with open(white_list_dir, 'r') as f:
        for line in f:
            white_list.append(line.strip())
    result_list = list()
    for exclude_barrier_circuit_call, line_number in exclude_barrier_circuit_call_list:
        method_call = exclude_barrier_circuit_call.split(".")[1].strip().split("(", 1)[0].strip()
        if method_call not in white_list:
            result_list.append((exclude_barrier_circuit_call, line_number))
    return result_list


def find_smell_212(my_parsed_object, my_circuit_bit_object, call_order_line_list):
    if not initial_check(my_parsed_object.get_file_dir()):
        return []
    function_implementation_dict = my_parsed_object.get_function_implementation_dict()
    result_list = list()
    for current_index in range(len(call_order_line_list)):
        current_line, current_line_number = call_order_line_list[current_index]
        if 'def ' in current_line or '.' not in current_line or not is_call_statement(current_line):
            continue
        line_scope, line_scope_name = find_line_scope(current_line_number, my_parsed_object.line_info_dict)
        variable, statement = get_left_right(current_line.strip())

        method_call_object_name, function_call_pure_name = analysis_call_statement(statement)
        # print("method call object name = ", method_call_object_name)
        if is_contain_circuit_name(my_circuit_bit_object, method_call_object_name, line_scope, line_scope_name):
            result_list.append((current_line, current_line_number))
            continue
        parameter_local_variable_convert_list = my_parsed_object.get_function_parameter_variable_associate_dict()[line_scope_name]
        for function_signature_parameter_name, local_variable_name, scope, scope_name in parameter_local_variable_convert_list:
            if function_signature_parameter_name != method_call_object_name and local_variable_name != method_call_object_name:
                continue
            function_signature, function_line_number = function_implementation_dict[line_scope_name][0]
            parameter_index = find_signature_parameter_index(function_signature, function_signature_parameter_name)
            if is_contain_global_call_source_variable(call_order_line_list[:current_index], method_call_object_name, line_scope_name, parameter_index, my_parsed_object, my_circuit_bit_object):
                result_list.append((current_line, current_line_number))
                break
    print("all gate list = ", result_list)
    return result_list