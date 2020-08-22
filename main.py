import json
import re

from search import get_best_k_completions
from init_data_structure import write_to_files

size_of_string = 7
size_of_res = 5

def print_result(json_lines, auto_list):
    for i in auto_list:
        line = json_lines[str(i.file_id)][str(i.offset)]
        print(
            f'\t\033[35m\033[1m{line[:len(line) - 1]}\033[0m    ,\033[37m( file:\033[94m\033[4m{i.source_text}\033[0m\033[37m ) ,(arg:{i.offset})\033[0m')
def run(json_data, json_lines):
    print("Hi user!")
    while 1:
        input_user = input("\nPlease enter the string you want us to search for you or enter exit\n")
        if input_user == "exit":
            print("GoodBye:)")
            break
        print_result(json_lines,
                     get_best_k_completions(json_data, json_lines,
                                            re.sub(r"[^a-z0-9]+", ' ', input_user.lower()[:size_of_string])) [:size_of_res])
        while 1:
            input_user += input(input_user)
            if input_user[-1] == '#':
                break
            print_result(json_lines,
                         get_best_k_completions(json_data, json_lines,
                                                re.sub(r"[^a-z0-9]+", ' ', input_user.lower()[:size_of_string])) [:size_of_res])


def read_from_file():
    file_data = open("data2.json")
    json_data = json.load(file_data)
    file_data.close()
    file_data = open("line2.json")
    json_lines = json.load(file_data)
    file_data.close()
    return json_data, json_lines


if __name__ == '__main__':
    # write_to_files()
    file = read_from_file()
    run(file[0], file[1])
