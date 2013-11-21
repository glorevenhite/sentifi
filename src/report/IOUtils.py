import csv
import io
from PathUtils import *


class IOUtils(object):

    @staticmethod
    def read_list_from_csv(file_path):
        results = []

        f = open(file_path, "rU")

        try:
            reader = csv.reader(f, delimiter=",", dialect='excel')
            for row in reader:
                results.append(row)
        except IOError:
            print IOError

        f.close()

        return results

    #Data is the first column in csv file
    @staticmethod
    def read_first_column_in_csv(file_path):
        results = []

        f = open(file_path, "rU")

        try:
            reader = csv.reader(f, delimiter=",", dialect='excel')
            for row in reader:
                results.append(row[0])
        except IOError:
            print IOError

        f.close()

        return results

    @staticmethod
    def read_nth_column_in_csv(file_path, nth):
        results = []

        f = open(file_path, "rU")

        try:
            reader = csv.reader(f, delimiter=",", dialect='excel')
            for row in reader:
                results.append(row[nth])
        except IOError:
            print IOError

        f.close()

        return results

    @staticmethod
    def save_list_to_csv(header, list_contents, file_path):
        #Create file_path if the file doesn't exist
        #PathUtils().create_path_if_not_exists(file_path)

        f = open(file_path, 'ab')    #Appending file
        wr = csv.writer(f, dialect='excel')

        #write down the header first
        if header is not None:
            wr.writerow(header)

        for row in list_contents:
            try:
                wr.writerow(row)
            except IOError:
                print IOError

        f.close()

    @staticmethod
    def save_json_data_to_file(json_data, file_name, dir_path):
        f = io.open(dir_path + file_name, 'w', encoding='utf-8')

        f.write(unicode(json_data))

        f.close()

    #Combine all files in same directory into a master files
    def combine_csv_file_in_same_dir(self, dir_path, has_header):
        results = []

        file_names = get_list_filename(dir_path)

        for f in file_names:
            contents = []
            if has_header:
                contents = self.read_list_from_csv(dir_path + f)
                #remove header
                del contents[0]
                print len(contents)
            results.extend(contents)

        #remove duplication
        results = self.remove_duplication_list(results)
        return results

    @staticmethod
    def remove_duplication_list(list_item):
        dict_item = {}
        for item in list_item:
            dict_item.update({item[0]: item})

        len(dict_item.values())
        return dict_item.values()

#PATH = "D:\\online-cloud\\Dropbox\\Sentifi Analytics\\5. Dan\\Treasury Bill\\"
#has_header = True
#list = IOUtils().combine_csv_file_in_same_dir(PATH, has_header)
#IOUtils().save_list_to_csv(None, list, "D:\combine.csv")
#print len(list)