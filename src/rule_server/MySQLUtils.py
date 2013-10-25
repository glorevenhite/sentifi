import MySQLdb as mdb
from IOUtils import IOUtils
from Constant import SQLTableName

class MySQLUtils(object):
    def __init__(self):
        SERVER = '127.0.0.1'
        USERNAME = 'root'
        PASSWORD = ""
        DBNAME = "autocategory_db"
        self.connection = None
        self.cursor = None

        self.connection = mdb.connect(SERVER, USERNAME, PASSWORD, DBNAME)
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
            results.append(row[0]) #taking the first one

        return results

    #Selecting using query string
    def select_query(self, str_query):
        self.cursor.execute(str_query)
        return self.cursor.fetchall()


"""table_name = "temp_0915_stickers"

PATH = "D:\\"
file_name = "combine.csv"

values = IOUtils().read_list_from_csv(PATH + file_name)
col_names = ['profile_id', 'twitter_fullname', 'twitter_screen_name',
             'image_url', 'joined', 'url', 'lang', 'location', 'twitter_description',
             'followers', 'friends', 'updates', 'listed', 'protected', 'verified', 'lasttweet', 'lasttweetdate']
var_list = []
for v in values[0]:
    var_list.append(unicode(v).encode('utf-8'))

var_string = ','.join("?"*len(var_list))
query_string = 'INSERT INTO ' + table_name + ' VALUES(%s);' % var_string

print len(query_string)
#sql = "INSERT INTO table VALUES %r;" %(tuple(var_list),)
print len(values[0])
cursor = MySQLUtils('sentifi_category').insert(col_names, values[0], table_name)
"""


#print cursor.execute("INSERT INTO Test VALUES(1,1)")
