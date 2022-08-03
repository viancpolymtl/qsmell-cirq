def is_target_call(pure_name, target_call_name_list, type_name_list, iterable_type):
    return pure_name in target_call_name_list and set(type_name_list).intersection(set(iterable_type))


def find_smell_211(title):
    target_call_name_list = ['Unitary', 'Hamiltonian', 'SingleQubitUnitary']
    iterable_type = ['list', 'tuple', 'dict', 'set']
    smell_count = 0
    call_split_list = title.split(';')
    call_split_list = list(filter(lambda x: (x.strip() != ""), call_split_list))
    for call in call_split_list:
        pure_name = call.split("(", 1)[0].strip()
        type_name_list = call.split("(", 1)[1].strip().split(")", 1)[0].strip().split(",")
        if is_target_call(pure_name, target_call_name_list, type_name_list, iterable_type):
            smell_count += 1
    return smell_count