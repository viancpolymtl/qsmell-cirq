from helper import *
from base_util import *


def is_target_call_variable(call_statement, class_call_name):
    """ This function checks if the class_call_name in call statement."""

    # Class call name: QuantumCircuit
    # call statement: The line statement
    return class_call_name + '(' in call_statement


def analyze_multi_call_statement(call_list):
    ''' for a().b().c(), return a, [b,c] '''
    method_call_object_name = call_list[0].split("(", 1)[0].strip()
    call_statement_list = list()
    for call in call_list[1:]:
        if '()' in call:
            pure_name = call.split("(")[0].strip()
        else:
            pure_name = call
        call_statement_list.append(pure_name)
    return method_call_object_name, call_statement_list


def find_class_call_count(class_call_name, candidate_method_lists, call_order_line_list, function_implementation_dict):
    possible_call_variable_list = list()
    count = 0
    for call_statement, line_number in call_order_line_list:
        variable, statement = get_left_right(call_statement)
        if '.' in statement and statement.count("()") == 1:
            method_call_object_name, method_call_statement = statement.split('.', 1)
            if method_call_object_name not in possible_call_variable_list:
                continue
            method_call_statement = method_call_statement.split("(")[0].strip()
            if method_call_statement in candidate_method_lists:
                count += 1
        elif '.' in statement and statement.count("()") > 1:
            call_list = statement.split('.')
            method_call_object_name, call_list = analyze_multi_call_statement(call_list)
            if method_call_object_name == class_call_name and set(call_list).intersection(set(candidate_method_lists)) != 0:
                count += 1
        elif is_target_call_variable(call_statement, class_call_name) and variable is not None and '.' not in call_statement and '(' in call_statement:
            possible_call_variable_list.append(variable)
        elif '(' in call_statement and '.' not in call_statement:
            parameter_list = build_statement_call_parameter_list(call_statement)
            index_list = list()
            for index, parameter in enumerate(parameter_list):
                if parameter in possible_call_variable_list:
                    index_list.append(index)
            call_name = call_statement.split("(", 1)[0].strip()
            if call_name not in function_implementation_dict:
                continue
            function_signature, function_start_line_number = function_implementation_dict[call_name][0]
            function_signature_parameter_list = function_signature.split("(", 1)[1].strip().split(")", 1)[0].split(',')
            for index in index_list:
                possible_call_variable_list.append(function_signature_parameter_list[index])
    return count



def find_smell_221(my_parsed_object, call_order_line_list):
    keyword_list = load_keyword_list()
    keyword_class_call_dict = build_keyword_class_call_dict(keyword_list)
    result_dict = defaultdict(int)
    #  keyword_class_call_dict: key: class_call_name, value: possible method names; i.e. a list
    function_implementation_list_dict = my_parsed_object.get_function_implementation_dict()
    for class_call_name in keyword_class_call_dict:
        candidate_method_lists = keyword_class_call_dict[class_call_name]
        class_call_count = find_class_call_count(class_call_name, candidate_method_lists, call_order_line_list,
                                                 function_implementation_list_dict)
        result_dict[class_call_name] = class_call_count
    result_dict = dict(result_dict)
    smell_val = 0
    for call in result_dict:
        smell_val += result_dict[call]
    return smell_val