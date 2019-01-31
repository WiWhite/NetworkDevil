import os
import difflib


basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
maindir = os.path.join(basedir, 'BACKUPS')


def files_for_diff(namedir):
    
    files_list = os.listdir(namedir)
    full_list = [os.path.join(namedir, file) for file in files_list]
    sorted_list = sorted(full_list, key=os.path.getmtime)

    return sorted_list[-2:]

def difffiles(listfiles):

    with open(listfiles[0], 'r') as file1, open(listfiles[1], 'r') as file2:
        file1split = file1.read().splitlines()
        file2split = file2.read().splitlines()
        d = difflib.Differ()
        diff = d.compare(file1split, file2split)
        return diff

def show_diff(namedir):

    for line in difffiles(files_for_diff(namedir)):
        print(line)
