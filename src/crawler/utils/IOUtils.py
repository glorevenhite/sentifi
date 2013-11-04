import csv
import io
from PathUtils import PathUtils


class IOUtils(object):

    @staticmethod
    def read_list_from_csv(file_path):
        results = []

        f = open(file_path, "rU")

        try:
            reader = csv.reader(file, delimiter=",", dialect='excel')
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
            reader = csv.reader(file, delimiter=",", dialect='excel')
            for row in reader:
                results.append(row[0])
        except IOError:
            print IOError

        f.close()

        return results

    @staticmethod
    def save_list_to_csv(header, list_contents, file_path):
        #Create file_path if the file doesn't exist
        PathUtils().create_path_if_not_exists(file_path)

        #Appending file
        f = open(file_path, 'ab')
        wr = csv.writer(file, dialect='excel')

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
    def save_json_data_to_file(json_data, file_name, path):
        f = io.open(path + file_name, 'w', encoding='utf-8')

        f.write(unicode(json_data))

        f.close()

    @staticmethod
    def save_objects_to_csv(objects, file_path):
        pass

    #Combine all files in same directory into a master files
    @staticmethod
    def combine_csv_file_in_same_dir(self, path, has_header):
        results = []

        file_names = PathUtils().get_list_filename(path)

        for file_name in file_names:
            contents = []
            if has_header:
                contents = self.read_list_from_csv(path + file_name)
                #remove header
                del contents[0]
                print len(contents)
            results.extend(contents)

        #remove duplication
        results = self.remove_duplication_list(results)
        return results

    @staticmethod
    def remove_duplication_list(list_items):
        dict_result = {}
        for item in list_items:
            dict_result.update({item[0]: item})

        len(dict_result.values())
        return dict_result.values()

#PATH = "D:\\online-cloud\\Dropbox\\Sentifi Analytics\\5. Dan\\Treasury Bill\\"
#has_header = True
#list = IOUtils().combine_csv_file_in_same_dir(PATH, has_header)
#IOUtils().save_list_to_csv(None, list, "D:\combine.csv")
#print len(list)