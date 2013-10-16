import os
import csv
import json
import io
from os import path
import pprint

class IOUtils(object):
    def read_list_from_csv(self, file_path):
        results = []

        file = open(file_path, "rb")

        try:
            reader = csv.reader(file, dialect="excel", delimiter=",")
            for row in reader:
                results.append(row)
        except IOError:
            print IOError

        file.close()

        return results

    def save_list_to_csv(self, header, list_contents, file_path):
        #Create file_path if the file doesn't exist
        self.create_path_if_not_exists(file_path)

        file = open(file_path, 'ab')    #Appending file
        wr = csv.writer(file, dialect='excel')

        #write down the header first
        wr.writerow(header)

        for row in list_contents:
            try:
                wr.writerow(row)
            except IOError:
                print IOError

        file.close()

    def save_json_data_to_file(self, json_data, file_path):
        file = io.open('file_path','w', encoding='utf-8')
        file.write(unicode(json.encoder(json_data, ensure_ascii = False)))
        file.close()

    def create_path_if_not_exists(self, file_path):
        if not path.exists(path.dirname(file_path)):
            os.makedirs(path.dirname(file_path))

    def save_objects_to_csv(self, objects, file_path):
        pass

