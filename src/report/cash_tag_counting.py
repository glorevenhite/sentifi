from re import match

__author__ = 'vinh.vo@sentifi.com'

from IOUtils import IOUtils
import re

file_path = "D:\\Dropbox\\Sentifi Analytics\\5. Vinh\\20131118_for_MM-from_new_hashtags.csv"
column = 14

list_tags = IOUtils.read_nth_column_in_csv(file_path, column)

s_tag_regex = re.compile('^\\$')
h_tag_regex = re.compile('^\\#')
a_tag_regex = "^\\@"

result_set = []
for row in list_tags:
    list_tags = row.split(",")
    list_s_tag = []
    count_s = 0
    list_h_tag = []
    count_h = 0
    list_a_tag = []
    count_a = 0

    result_row = []

    list_s_tag = [tag for tag in row.split(",") if re.match(s_tag_regex, tag)]
    count_s = row.count("$")

    list_h_tag = [tag for tag in row.split(",") if re.match(h_tag_regex, tag)]
    count_h = row.count("#")

    list_a_tag = [tag for tag in row.split(",") if re.match(a_tag_regex, tag)]
    count_a = row.count("@")

    result_row = [",".join(list_s_tag), count_s, ",".join(list_h_tag), count_h, ",".join(list_a_tag), count_a]
    result_set.append(result_row)

IOUtils.save_list_to_csv(['list $', 'count', 'list_#', 'count', 'list_@', 'count'], result_set, "D:\\results.csv")










