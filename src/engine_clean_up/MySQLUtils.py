import MySQLdb as mdb
from Constant import *
from IOUtils import IOUtils
from SentifiTwitterProfile import SentifiTwitterProfile


class MySQLUtils(object):
    def __init__(self):
        self.connection = None
        self.cursor = None

        self.connection = mdb.connect(SERVER, USERNAME, PASSWORD, DATABASE_NAME, charset='utf8')
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

#conn = MySQLUtils().connection
#cur = conn.cursor()
#query = "SELECT * FROM tbl_uncategorized_searched_profiles_from_twitter_results"
#cur.execute(query)
#rows = cur.fetchall()
#file_name = 'tbl_uncategorized_searched_profiles_from_twitter_results.csv'

#print len(rows)
#for row in rows:
#    list_content = []
#    list_content.append([unicode(col).encode('utf-8') for col in row])
#    IOUtils().save_list_to_csv(None, list_content, file_name)
#    #p.display()
#
#print len(list_content)

#IOUtils().save_list_to_csv(None, list_content, file_name)

