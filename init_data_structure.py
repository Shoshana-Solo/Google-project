import os
from collections import defaultdict
import re
import json

size_of_string = 7
data = defaultdict(list)
lines = defaultdict(dict)
count_file = 0
size_of_res = 5


def insert_as_dict(str_file, path):
    lines[count_file]['path'] = path
    for index_line, line in enumerate(str_file.readlines()):
        lines[count_file][index_line] = line
        line = re.sub(r"[^a-z0-9]+", ' ', line.lower())
        for i in range(len(line)):
            for j in range(size_of_string + 1):
                if i + j < len(line) + 1:
                    if len(data[line[i:i + j]]) < size_of_res:
                        data[line[i:i + j]].append((count_file, index_line))


def init_data(folder):
    global count_file
    directory = os.path.normpath(folder)
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            file_ = open(os.path.join(subdir, file), encoding="utf8")
            insert_as_dict(file_, os.path.join(subdir, file))
            file_.close()

            count_file += 1


def write_to_files():
    init_data("data")
    with open("data2.json", "w") as outfile:
        json.dump(data, outfile)
    with open("line2.json", "w") as outfile:
        json.dump(lines, outfile)
