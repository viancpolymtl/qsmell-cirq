from helper import *
from base_util import *


def build_import_list(call_order_line_list):
    result_list = list()
    for current_index in range(len(call_order_line_list)):
        current_line, current_line_number = call_order_line_list[current_index]
        if "import " in current_line:
            result_list.append((current_line.strip(), current_line_number))
    return result_list


def initial_check(call_order_line_list):
    from_import_list = build_import_list(call_order_line_list)
    pure_import_list = list()
    for from_import_statement, line_number in from_import_list:
        if 'from ' in from_import_statement:
            imported_part = from_import_statement.split("import ", 1)[1].strip()
            if "from qiskit" in from_import_statement and "transpile" in imported_part:
                return True
        else:
            pure_import_list.append(from_import_statement.strip())
    for pure_import_statement in pure_import_list:
        if 'qiskit' in pure_import_statement:
            return True
    return False


def find_smell_236(call_order_line_list):
    if not initial_check(call_order_line_list):
        return 0
    result = 1
    for current_index in range(len(call_order_line_list)):
        current_line, current_line_number = call_order_line_list[current_index]
        if 'def ' in current_line or not is_call_statement(current_line):
            continue
        variable, statement = get_left_right(current_line.strip())
        method_call_object_name, function_call_pure_name = analysis_call_statement(statement)
        if function_call_pure_name == 'transpile':
            parameter_list = statement.split("transpile(", 1)[1].strip().split(")", 1)[0].strip().split(",")
            for parameter in parameter_list:
                parameter = parameter.strip()
                parameter = parameter.replace(" ", '')
                if 'initial_layout=' in parameter:
                    break
            else:
                result = 0
    return result
