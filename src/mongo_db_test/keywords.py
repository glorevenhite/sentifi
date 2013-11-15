__author__ = 'vinh.vo@sentifi.com'

import urllib2
import simplejson
import pprint
import csv
import io


def save_list_to_csv(header, list_contents, file_path):
        #Create file_path if the file doesn't exist
        #PathUtils().create_path_if_not_exists(file_path)

        file = open(file_path, 'ab')    #Appending file
        wr = csv.writer(file, dialect='excel')

        #write down the header first
        if header is not None:
            wr.writerow(header)

        for row in list_contents:
            try:
                wr.writerow(row)
            except IOError:
                print IOError

        file.close()

url = 'http://sentifi.com/api/GetSearchItemInfo?searchitems=all&authkey=js520f35997438d6.70129732'
req = urllib2.Request(url, None)
opener = urllib2.build_opener()
f = opener.open(req)
json_data = simplejson.loads(f.read())

list_total_keywords = []
for item in json_data:
    keywords = item['keywords']
    #print keywords
    if keywords is not None:
        for kws in keywords:
            l_kw = kws['word']
            list_total_keywords.append([unicode(w).encode('utf-8') for w in l_kw.split(",")])

pprint.pprint(list_total_keywords)
save_list_to_csv(None, list_total_keywords, "D:\\kw.csv")



