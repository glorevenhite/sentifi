import MySQLdb as mdb
from Constant import *


class MySQLUtils(object):
    def __init__(self):
        SERVER = '127.0.0.1'
        USERNAME = 'root'
        PASSWORD = ""
        DBNAME = DATABASE_NAME
        self.connection = None
        self.cursor = None

        self.connection = mdb.connect(SERVER, USERNAME, PASSWORD, DBNAME, charset='utf8')
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT VERSION()")

        ver = self.cursor.fetchone()

        #print "Database version: %s" %ver

    #Inserting multi-values into multi-colums respectively
    def insert(self, col_names, values, table_name):
        #Creating a list of %s
        str = ['%s']*len(values)

        #Joining list of %s by comma
        var_st = ','.join(str)

        #Building query string
        query_str = 'INSERT INTO ' + table_name + ' VALUES(%s);' %var_st

        #Execute query and commit
        self.cursor.execute(query_str, values)
        self.connection.commit()

    #Selecting multi-columns from a table
    def select(self, list_column_names, table_name):

        #Joining the list of column names by comma
        list_column_name_in_string = ",".join(list_column_names)

        #Building query
        str_query = "SELECT %s" %list_column_name_in_string + " FROM %s" %table_name
        #print str_query

        #Execute query
        self.cursor.execute(str_query)

        return self.cursor.fetchall()

    #Selecting data from table using WHERE-clause. Just single pair(column, value) only
    def select_where(self, list_column_names, table_name, list_where_clauses):

        #Joining column name using comma
        list_column_name_as_string = ",".join(list_column_names)

        #Joining where clauses using equation sign (=)
        where_clauses_as_string = " = ".join(list_where_clauses)

        #Buiding query
        str_query =  "SELECT %s " %list_column_name_as_string
        str_query += "FROM %s " %table_name
        str_query += "WHERE %s " %where_clauses_as_string
        #print str_query

        #Execute query
        self.cursor.execute(str_query)
        rows = self.cursor.fetchall()

        #multi columns in each row, only taking the FIRST one.
        results = []
        for row in rows:
            results.append(row[0]) # taking the first one

        return results

    #Selecting using query string
    def select_query(self, str_query):
        self.cursor.execute(str_query)
        return self.cursor.fetchall()
