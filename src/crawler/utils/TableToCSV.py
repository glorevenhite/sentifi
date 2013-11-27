__author__ = 'vinh.vo@sentifi.com'

import sys
import MySQLdb
from IOUtils import IOUtils

SERVER = 'localhost'
USERNAME = 'root'
PASSWORD = 'qscwdv'
DATABASE = 'new_community'


def table_to_csv(table_name, file_name):
    sql = "SELECT * FROM {0} ".format(table_name)
    connection = MySQLdb.connect(SERVER, USERNAME, PASSWORD, DATABASE)
    cursor = connection.cursor()
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



