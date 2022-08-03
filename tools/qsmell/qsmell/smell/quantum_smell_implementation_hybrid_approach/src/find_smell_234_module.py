def find_smell_234(content):
    result_list = list()
    for row in content:
        row = row[0]
        row_list = row.split(';')
        row_list = list(filter(lambda x: (x.strip() != ""), row_list))
        tf_table = row_list[1:]
        index_list = list()
        for index, val in enumerate(tf_table):
            if val == '1':
                index_list.append(index)
                if len(index_list) == 2:
                    result_list.append(index_list)
                    break
    new_result_list = list()
    for inner_list in result_list:
        diff = inner_list[1] - inner_list[0]
        new_result_list.append(diff)
    return new_result_list
