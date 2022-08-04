import csv
import os
import sys
import logging, shutil, traceback
from find_smell_211_module import find_smell_211
from find_smell_231_module import find_smell_231
from find_smell_232_module import find_smell_232
from find_smell_233_module import find_smell_233
from find_smell_234_module import find_smell_234


def create_folder_safely(folder_dir: str) -> None:
    """
    Safely create given folder directory
    :param folder_dir: The directory of the folder we want to create
    :return: None
    """
    try:
        os.mkdir(folder_dir)
    except FileExistsError:
        shutil.rmtree(folder_dir)
        os.mkdir(folder_dir)
    except Exception as e:
        logging.error(traceback.format_exc())


def main():
    if len(sys.argv) != 3:
        print("Insufficient Amount of arguments")
        exit(0)
    csv_root_dir = sys.argv[1]
    result_folder_dir = sys.argv[2]
    create_folder_safely(result_folder_dir)
    task_name_list = ["Usage_of_customized_gates_result.csv", "Long_circuit_result.csv", "Intermediate_measurements_result.csv", "Idle_qubits_result.csv", "Initialization_of_qubits_differently_result.csv"]
    call_function_list = ['find_smell_211(title)', 'find_smell_231(title, content)', 'find_smell_232(title)', 'find_smell_233(content)', 'find_smell_234(content)']
    for result_file_name, call in zip(task_name_list, call_function_list):
        with open(result_folder_dir + result_file_name, 'w+') as f:
            writer = csv.writer(f)
            task_name = result_file_name.split('.csv')[0].strip()
            writer.writerow(["File_name", task_name])
            for csv_file_name in os.listdir(csv_root_dir):
                with open(csv_root_dir + csv_file_name, 'r') as g:
                    reader = list(csv.reader(g))
                    title = reader[0][0]
                    content = reader[1:]
                    writer.writerow([csv_file_name, eval(call)])


if __name__ == '__main__':
    main()
