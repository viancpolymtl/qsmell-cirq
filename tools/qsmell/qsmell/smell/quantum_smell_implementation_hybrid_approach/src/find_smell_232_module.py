def find_smell_232(title):
    call_split_list = title.split(';')
    call_split_list = list(filter(lambda x: (x.strip() != ""), call_split_list))
    pure_call_name_list = list()
    for call in call_split_list:
        pure_call_name_list.append(call.split("(", 1)[0].strip())
    if 'measure' in pure_call_name_list:
        first_measure_index = pure_call_name_list.index('measure')
        sublist = pure_call_name_list[first_measure_index+1:]
        for sub_call in sublist:
            if sub_call != 'measure':
                return 1
        return 0
    else:
        return 0
