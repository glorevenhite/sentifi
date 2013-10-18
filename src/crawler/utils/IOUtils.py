import os
import csv
import json
import io
import pprint

from os import path
from PathUtils import PathUtils

class IOUtils(object):

    def read_list_from_csv(self, file_path):
        results = []

        file = open(file_path, "rU")

        try:
            reader = csv.reader(file, delimiter=",", dialect='excel')
            for row in reader:
                results.append(row)
        except IOError:
            print IOError


        file.close()

        return results

    def save_list_to_csv(self, header, list_contents, file_path):
        #Create file_path if the file doesn't exist
        PathUtils().create_path_if_not_exists(file_path)

        file = open(file_path, 'ab')    #Appending file
        wr = csv.writer(file, dialect='excel')

        #write down the header first
        if (header != None):
            wr.writerow(header)

        for row in list_contents:
            try:
                wr.writerow(row)
            except IOError:
                print IOError

        file.close()

    def save_json_data_to_file(self, json_data, json_data_id, path):
        file = io.open(path + json_data_id, 'w', encoding='utf-8')

        file.write(unicode(json.encoder(json_data, ensure_ascii = False)))

        file.close()

    def save_objects_to_csv(self, objects, file_path):
        pass

    #Combine all files in same directory into a master files
    def combine_csv_file_in_same_dir(self, path, has_header):
        results = []

        filenames = PathUtils().get_list_filename(path)

        for file in filenames:
            contents = []
            if(has_header):
                contents = self.read_list_from_csv(path + file)
                #remove header
                del contents[0]
                print len(contents)
            results.extend(contents)

        #remove duplication
        results = self.remove_duplication_list(results)
        return results

    def remove_duplication_list(self, list):
        dict = {}
        for item in list:
            dict.update({item[0]:item})

        len(dict.values())
        return dict.values()

#PATH = "D:\\online-cloud\\Dropbox\\Sentifi Analytics\\5. Dan\\Treasury Bill\\"
#has_header = True
#list = IOUtils().combine_csv_file_in_same_dir(PATH, has_header)
#IOUtils().save_list_to_csv(None, list, "D:\combine.csv")
#print len(list)