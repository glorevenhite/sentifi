__author__ = 'vinh.vo@sentifi.com'

import sys
import MySQLdb
from IOUtils import IOUtils
import csv


SERVER = 'localhost'
USERNAME = 'root'
PASSWORD = 'qscwdv'
DATABASE = 'new_community'


def csv_to_table(file_name, table):
    list_content = IOUtils.read_list_from_csv(file_name)
    header = list_content[0]


    sql = "SELECT * FROM {0} ".format(table_name)
    connection = MySQLdb.connect(SERVER, USERNAME, PASSWORD, DATABASE)
    cursor = connection.cursor()

    csv_data = csv.reader(file(file_name))

    for row in csv_data:

    cursor.execute(sql)
    rows = cursor.fetchall()

    list_content = []
    for row in rows:
        list_row = list(row)
        list_content.append(list_row)

    IOUtils.save_list_to_csv(None, list_content, file_name)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        table_name = sys.argv[1]
        file_name = sys.argv[2]



