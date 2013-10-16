from os import listdir
from os.path import isfile, join

class PathUtils(object):

    def get_list_filename(path):
        return [f for f in listdir(path) if isfile(join(path,f))]

    def create_path_if_not_exists(self, file_path):
        if not path.exists(path.dirname(file_path)):
            os.makedirs(path.dirname(file_path))