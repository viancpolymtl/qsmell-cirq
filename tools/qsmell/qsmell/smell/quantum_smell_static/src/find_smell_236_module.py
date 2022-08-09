from helper import *
from base_util import *


def build_import_list(full_contents):
    result_list = list()
    for current_line_number, current_line in enumerate(full_contents):
        if "import " in current_line:
            result_list.append((current_line.strip(), current_line_number))
    return result_list


def initial_check(full_contents):

    from_import_list = build_import_list(full_contents)
    pure_import_list = list()
    print("from import list = ", from_import_list)
    for from_import_statement, line_number in from_import_list:
        print("from_import = ", from_import_statement)
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


def find_smell_236(file_dir):
    with open(file_dir, 'r') as f:
        full_contents = f.readlines()
    if not initial_check(full_contents):
        return "N/A"

    result = 0
    for current_line_number, current_line in enumerate(full_contents):
        if 'def ' in current_line or not is_call_statement(current_line):
            continue
        variable, statement = get_left_right(current_line.strip())
        method_call_object_name, function_call_pure_name = analysis_call_statement(statement)
        print("statement = ", statement)
        if function_call_pure_name == 'transpile':
            parameter_list = statement.split("transpile(", 1)[1].strip().split(")", 1)[0].strip().split(",")
            for parameter in parameter_list:
                parameter = parameter.strip()
                parameter = parameter.replace(" ", '')
                if 'initial_layout=' in parameter:
                    break
            else:
                result += 1
    return str(result)
