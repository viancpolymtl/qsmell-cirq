from collections import defaultdict
import numpy


def find_max_num_ops(title):
    title_list = title.split(';')
    title_list = list(filter(lambda x: (x.strip() != ""), title_list))
    count_dict = defaultdict(int)
    for title in title_list:
        pure_name = title.split('(', 1)[0].strip()
        count_dict[pure_name] += 1
    sorted_x = sorted(count_dict.items(), key=lambda kv: kv[1])
    return sorted_x[0][1]


def find_max_num_parallel_ops(content):
    y = numpy.array([numpy.array(xi) for xi in content])
    z = numpy.transpose(y)
    max_count = 0
    for inner_arr in z:
        current_count = numpy.count_nonzero(inner_arr == '1')
        if current_count > max_count:
            max_count = current_count
    return max_count


def rebuild_content(content):
    result_content = list()
    for row in content:
        row = row[0]
        row_list = row.split(';')
        row_list = list(filter(lambda x: (x.strip() != ""), row_list))
        tf_table = row_list[1:]
        result_content.append(tf_table)
    return result_content


def find_smell_231(title, content):
    content = rebuild_content(content)
    max_number_ops = find_max_num_ops(title)
    max_number_parallel_ops = find_max_num_parallel_ops(content)
    return max_number_ops * max_number_parallel_ops