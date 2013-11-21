import os
from os import path
from os import listdir
from os.path import isfile, join


def get_list_filename(dir_path):
    return [f for f in listdir(dir_path) if isfile(join(dir_path, f))]


def create_path_if_not_exists(file_path):
    if not path.exists(path.dirname(file_path)):
        os.makedirs(path.dirname(file_path))