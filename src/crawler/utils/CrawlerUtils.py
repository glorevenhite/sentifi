import os
import csv
from os import path
import pprint
from utils.IOUtils import *

class CrawlerUtils(object):
    def read_screen_names_from_csv_file(self, file_path):
        return IOUtils().read_list_from_csv(file_path)

    #split a LIST into CHUNK having N elements
    def split_into_chunks(self, list, n):
        for i in xrange(0, len(list), n):
            yield list[i:i+n]

    def parse_tweepy_user_object_to_json(self, user):
        return jsonpickle.encode(user)# Replacing text in given string

    def rreplace(self,s, old, new, occurrence):
        li = s.rsplit(old, occurrence)
        return new.join(li)


