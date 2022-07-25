import keyword


def read_file(file_dir):
    with open(file_dir, 'r') as f:
        file_content = f.read()
    return file_content


def find_line_scope(line_count, line_info_dict):
    for line, scope, name in line_info_dict:
        start_line_num, end_line_num = line_info_dict[(line, scope, name)]
        if start_line_num <= line_count <= end_line_num:
            return scope, name
    return 'global', None


def get_left_right(call_statement):
    if '=' in call_statement and '(' in call_statement:
        if call_statement.index('=') > call_statement.index("("):
            return None, call_statement
    if '=' in call_statement:
        left, right = call_statement.split('=', 1)
        left = left.strip()
        right = right.strip()
    else:
        left = None
        right = call_statement.strip()
    return left, right


def build_my_keyword_list():
    my_keyword_list = list(keyword.kwlist)
    my_keyword_list.remove("True")
    my_keyword_list.remove("False")
    my_keyword_list.append("else:")
    my_keyword_list.remove("for")
    return my_keyword_list


def is_contain_circuit_name(my_circuit_bit_object, call_object_name, current_scope, current_scope_name):
    file_defined_circuit_name_list = my_circuit_bit_object.get_file_defined_circuit_list()
    file_infectious_circuit_name_list = my_circuit_bit_object.get_file_infectious_circuit_name_list()
    for circuit_name, scope, name in file_defined_circuit_name_list:
        if circuit_name == call_object_name:
            if current_scope == scope and current_scope_name == name:
                return True
            elif scope == 'global':
                return True

    for source_circuit, destination_circuit, scope, name in file_infectious_circuit_name_list:
        if source_circuit == call_object_name or destination_circuit == call_object_name:
            if current_scope == scope and current_scope_name == name:
                return True
            elif scope == 'global':
                return True
    return False


def build_parameter_list_from_call_helper(current_call):
    """ This function builds the parameter list from a call i.e. main(a, b) """
    parameter_list = current_call.split("(")[1].strip().split(")")[0].strip().split(',')
    parameter_list_sp = list()
    for parameter in parameter_list:
        if parameter.startswith('[') or parameter.endswith(']'):
            x = parameter.split('[')[0].strip()
            x = x.replace('[', '')
            parameter_list_sp.append(x.strip())
    if len(parameter_list_sp) != 0:
        parameter_list_sp = list(set(parameter_list_sp))
        parameter_list_sp = list(filter(lambda x:(x.strip()!=""), parameter_list_sp))
        return parameter_list_sp

    if ',' not in parameter_list:
        if '[' in parameter_list[0]:
            parameter_list[0] = parameter_list[0].split('[', 1)[0].strip()
    if '[' not in current_call:
        parameter_list = list(filter(lambda x: (x.strip() != ""), parameter_list))
        parameter_list = list(map(lambda x: (x.strip()), parameter_list))
        return parameter_list
    current_special_param_str = ""
    result_parameter_list = list()
    for index in range(len(parameter_list)):
        parameter = parameter_list[index].strip()
        if '[' not in parameter and ']' not in parameter:
            result_parameter_list.append(parameter)
        elif '[' in parameter:
            current_special_param_str += parameter
        elif ']' in parameter:
            current_special_param_str += parameter
            result_parameter_list.append(current_special_param_str)
            current_special_param_str = ""
    parameter_list = result_parameter_list

    parameter_list = list(filter(lambda x: (x.strip() != ""), parameter_list))
    parameter_list = list(map(lambda x: (x.strip()), parameter_list))
    parameter_list_final = list()
    for parameter in parameter_list:
        if '=' in parameter:
            parameter = parameter.split('=', 1)[1].strip()
        parameter_list_final.append(parameter)
    return parameter_list_final