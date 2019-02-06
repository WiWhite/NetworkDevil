import os
import difflib
import sys


def files_for_diff(namedir):

    try:
        files_list = os.listdir(namedir)
        full_list = [os.path.join(namedir, file) for file in files_list]
        if len(full_list) < 2:
            return full_list * 2
        else:
            sorted_list = sorted(full_list, key=os.path.getmtime)
            return sorted_list[-2:]
    except FileNotFoundError:
        exit(1)


def difffiles(listfiles):

    with open(listfiles[0], 'r') as file1, open(listfiles[1], 'r') as file2:
        file1split = file1.readlines()
        file2split = file2.readlines()
        diff = difflib.HtmlDiff().make_file(file1split, file2split)
        return diff


def show_diff(namedir):

    table = difffiles(files_for_diff(namedir))
    return table
