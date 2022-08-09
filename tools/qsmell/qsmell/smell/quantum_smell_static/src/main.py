import csv
import os
import sys

from find_smell_221_module import find_smell_221
from find_smell_236_module import find_smell_236
from helper import *
from parse_circuit_bit_info_module import *


def parse_file(file_dir):
    my_parsed_object = MyAstParser(file_dir)
    my_parsed_object.parse_file()
    return my_parsed_object


def parse_circuit_bit_info(my_parsed_object):
    my_circuit_bit_object = MyCircuitBitParser(my_parsed_object)
    my_circuit_bit_object.parse_file()
    return my_circuit_bit_object


def main():
    if len(sys.argv) != 3:
        print("Not enough arguments")
        exit(0)
    input_root_dir = sys.argv[1]
    result_csv_root_dir = sys.argv[2]
    create_folder_safely(result_csv_root_dir)
    title_list = ["Non-parameterized_circuit", "No-alignment_between_the_logical_and_physical_qubits"]
    call_list = ['find_smell_221(my_parsed_object, call_order_line_list)', 'find_smell_236(file_dir)']
    task_abbrev_list = ['NC', 'LPQ']
    for task_title, call, task_abbrev in zip(title_list, call_list, task_abbrev_list):
        result_csv_file_dir = result_csv_root_dir + task_abbrev + '_result.csv'
        with open(result_csv_file_dir, 'w+') as f:
            writer = csv.writer(f)
            writer.writerow(["File_Name", task_title])
            for file_name in os.listdir(input_root_dir):
                if not file_name.endswith(".py"):
                    continue
                print("doing file = ", file_name)
                file_dir = input_root_dir + file_name
                my_parsed_object = parse_file(file_dir)
                my_circuit_bit_object = parse_circuit_bit_info(my_parsed_object)
                call_order_line_list = build_call_order_line_list(my_parsed_object, my_circuit_bit_object)
                writer.writerow([file_name, eval(call)])


if __name__ == '__main__':
    main()
