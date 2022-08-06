import keyword
import re
import os
import logging
import traceback

from collections import OrderedDict, defaultdict
from base_util import *


def create_folder_safely(folder_dir: str) -> None:
    """
    Safely create given folder directory
    :param folder_dir: The directory of the folder we want to create
    :return: None
    """
    try:
        os.mkdir(folder_dir)
    except FileExistsError:
        os.rmdir(folder_dir)
        os.mkdir(folder_dir)
    except Exception as e:
        logging.error(traceback.format_exc())
        print("An exception occurred: {}".format(e))


def build_call_order_line_list(my_parsed_object, my_circuit_bit_object):
    global_call_list = my_parsed_object.get_global_full_statement_list()

    function_implementation_dict = my_parsed_object.get_function_implementation_dict()
    result_list = list()
    my_keyword_list = build_my_keyword_list()
    while len(global_call_list) != 0:
        full_statement_call, line_number = global_call_list[0]
        # print("full statement call = ", full_statement_call, " line number = ", line_number)
        # print("remain = ", len(global_call_list))
        full_statement_scope, full_statement_scope_name = find_line_scope(line_number, my_parsed_object.get_line_info_dict())
        global_call_list.pop(0)
        if full_statement_call.startswith("def "):
            result_list.append((full_statement_call, line_number))
            continue
        if full_statement_call.strip().startswith("#") or full_statement_call.strip() == '':
            continue
        if '# ' in full_statement_call.strip():
            full_statement_call = full_statement_call.split("#", 1)[0].strip()
        if '.' in full_statement_call and '(' in full_statement_call:
            call_object_name = full_statement_call.split('.', 1)[0].strip()
            if is_contain_circuit_name(my_circuit_bit_object, call_object_name, full_statement_scope, full_statement_scope_name):
                result_list.append((full_statement_call, line_number))
                continue
        statement_tokens = full_statement_call.split(' ')
        not_contain_keyword = all(i not in my_keyword_list for i in statement_tokens)
        if not_contain_keyword and '(' not in full_statement_call:
            result_list.append((full_statement_call, line_number))
            continue
        elif not not_contain_keyword and '(' not in full_statement_call and 'for ' not in full_statement_call:
            continue
        if '=' in full_statement_call and '(' not in full_statement_call:
            result_list.append((full_statement_call, line_number))
            continue
        call_name = full_statement_call.split("(", 1)[0].strip()
        if '=' in call_name:
            call_name = call_name.split("=", 1)[1].strip()
        if call_name not in function_implementation_dict and '.' not in call_name and not_contain_keyword:
            continue
        result_list.append((full_statement_call, line_number))
        if '.' not in call_name and call_name in function_implementation_dict:
            function_implementation_line_list = function_implementation_dict[call_name]
            # print("add: ", len(function_implementation_line_list))
            global_call_list = function_implementation_line_list + global_call_list

    return result_list


def analysis_call_statement(statement):
    """ This function takes a call statement, and gets the method call object name and function_pure_name """
    if '.' in statement:
        method_call_object_name, function_pure_name = statement.split(".", 1)
        method_call_object_name = method_call_object_name.strip()
        function_pure_name = function_pure_name.split("(", 1)[0].strip()
    else:
        method_call_object_name = None
        function_pure_name = statement.split('(', 1)[0].strip()
    return method_call_object_name, function_pure_name


def is_call_statement(statement):
    """ This function checks if it is a call i.e. hello() or a.b() """
    if '(' not in statement:
        return False
    else:
        index = statement.index('(')
        prev_char = statement[index-1]
        if prev_char == '.' or prev_char.isalpha():
            return True
        else:
            return False


def find_signature_parameter_index(function_signature, source_parameter_name):
    parameter_list = function_signature.split("(", 1)[1].strip().split(')', 1)[0].strip().split(",")
    parameter_list = list(filter(lambda x: (x.strip() != ''), parameter_list))
    try:
        return parameter_list.index(source_parameter_name)
    except ValueError:
        for index, parameter in enumerate(parameter_list):
            if '=' in parameter:
                parameter = parameter.split('=')[0].strip()
            if parameter == source_parameter_name:
                return index


def build_statement_call_parameter_list(original_statement):
    current_parameter_list = original_statement.split("(", 1)[1].strip()[:-1].strip().split(',')
    current_parameter_list_new = list()
    for current_parameter in current_parameter_list:
        if '=' in current_parameter:
            current_parameter = current_parameter.split('=', 1)[0].strip()
        if current_parameter.startswith('['):
            current_parameter = current_parameter[1:]
        current_parameter = current_parameter.split('[', 1)[0].strip()
        current_parameter_list_new.append(current_parameter)
    if 'None' in current_parameter_list_new:
        current_parameter_list_new.remove('None')
    if len(current_parameter_list_new) == 0:
        current_parameter_list_new = build_parameter_list_from_call_helper(original_statement)
        if 'None' in current_parameter_list_new:
            current_parameter_list_new.remove('None')
    current_parameter_list_new = list(OrderedDict.fromkeys(current_parameter_list_new))
    current_parameter_list_new = list(filter(lambda x: (x.strip() != ""), current_parameter_list_new))
    current_parameter_list_newest = list()
    for parameter in current_parameter_list_new:
        token_list = re.split("\W+", parameter)
        for token in token_list:
            current_parameter_list_newest.append(token)
    current_parameter_list_newest = list(OrderedDict.fromkeys(current_parameter_list_newest))

    last_index = -1
    for index, term in enumerate(current_parameter_list_newest):
        if term in keyword.kwlist:
            last_index = index

    current_parameter_list_best = current_parameter_list_newest[last_index + 1:]
    current_parameter_list_best = list(filter(lambda x: (x.strip()!=""), current_parameter_list_best))

    return current_parameter_list_best


def find_visiting_statement_target_parameter(visiting_statement_parameter_list, parameter_index, line_scope_name, my_parsed_object, method_call_object_name):
    try:
        visiting_statement_target_parameter = visiting_statement_parameter_list[parameter_index]
        return visiting_statement_target_parameter
    except IndexError:
        function_implementation_dict = my_parsed_object.get_function_implementation_dict()
        function_signature = function_implementation_dict[line_scope_name.strip()][0][0]
        parameter_list = function_signature.split("(", 1)[1].strip().split(")", 1)[0].strip().split(",")
        try:
            parameter = parameter_list[parameter_index]
            if '=' in parameter:
                return parameter.split("=")[0].strip()
            return parameter.strip()
        except IndexError:
            ''' using global case case '''
            return method_call_object_name


def convert_infectious_to_source(visiting_statement_target_parameter, file_infectious_bit_name_list):
    for source_parameter, destination_parameter, scope_name, name in file_infectious_bit_name_list:
        if destination_parameter == visiting_statement_target_parameter:
            return source_parameter


def extract_associated_parameter_name(parameter_call_associate_dict, current_parameter, current_line_scope_name):
    associated_call_parameter_list = parameter_call_associate_dict[current_line_scope_name]
    for parameter_source_name, current_parameter_dest, scope_name, function_name in associated_call_parameter_list:
        if current_parameter == current_parameter_dest:
            return parameter_source_name


def find_associated_parameter_index(associated_parameter_name, function_implementation_dict, current_line_scope_name, statement):
    function_signature, function_signature_line_number = function_implementation_dict[current_line_scope_name][0]
    call_parameter_name_list = function_signature.split("def ", 1)[1].strip().split("(", 1)[1].strip()[:-2].split(',')
    call_parameter_name_list = list(filter(lambda x: (x.strip() != ""), call_parameter_name_list))
    if associated_parameter_name in call_parameter_name_list:
        return call_parameter_name_list.index(associated_parameter_name)
    else:
        token_list = re.split("\W+", associated_parameter_name)
        for token in token_list:
            if token in call_parameter_name_list:
                return call_parameter_name_list.index(token)


def load_keyword_list():
    target_call_file_dir = "../resources/Built-in-Qiskit-Backend-Methods.txt"
    keyword_list = list()
    with open(target_call_file_dir, 'r') as f:
        for line in f:
            keyword_list.append(line.strip())
    return keyword_list


def build_keyword_class_call_dict(keyword_list):
    keyword_class_call_dict = defaultdict(list)
    for statement in keyword_list:
        class_call_name, method = statement.split(':', 1)
        keyword_class_call_dict[class_call_name].append(method)
    return keyword_class_call_dict


def is_loop(statement):
    for statement_token in statement.split():
        if statement_token.strip() in ['for', 'while']:
            return True
    return False


