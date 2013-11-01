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

    def get_rule_subset_by_phase_and_field(self, stage, field_id):
        sql = "SELECT DISTINCT c.name, rs.rule_set_id, r.rule_id, CONVERT(k.keyword USING utf8), r.type_not "
        sql += "FROM {0} AS c " .format(TABLE_CATEGORIES)
        sql += "JOIN {0} AS rs ON c.category_id = rs.category_id " .format(TABLE_RULESETS)
        sql += "JOIN {0} AS rsd ON rsd.rule_set_id = rs.rule_set_id " .format(TABLE_RULESET_DETAILS)
        sql += "JOIN {0} AS r ON r.rule_id = rsd.rule_id " .format(TABLE_RULES)
        sql += "JOIN {0} AS rk ON rk.rule_id = r.rule_id " .format(TABLE_RULE_KEYWORD)
        sql += "JOIN {0} AS k ON k.keyword_id = rk.keyword_id " .format(TABLE_KEYWORDS)
        sql += "JOIN {0} AS rf ON rf.rule_id = r.rule_id " .format(TABLE_RULE_FIELD)
        sql += "WHERE c.type LIKE '{0}' AND rf.field_id = {1} " .format(stage, field_id)

        print sql
        self.cursor.execute(sql)

        rows = self.cursor.fetchall()

        results = []
        for row in rows:    # OPTIMIZE HERE, return directly in tuple format instead of a list
            results.append(row)

        return results

    def get_rule_subset_by_phase_field_parent(self, stage, field_id, parent_id):
        sql = "SELECT DISTINCT c.name, rs.rule_set_id, r.rule_id, CONVERT(k.keyword USING utf8), r.type_not, p.name "
        sql += "FROM {0} AS c " .format(TABLE_CATEGORIES)
        sql += "JOIN {0} AS p ON p.category_id = c.parent_cat_id " .format(TABLE_CATEGORIES)
        sql += "JOIN {0} AS rs ON c.category_id = rs.category_id " .format(TABLE_RULESETS)
        sql += "JOIN {0} AS rsd ON rsd.rule_set_id = rs.rule_set_id " .format(TABLE_RULESET_DETAILS)
        sql += "JOIN {0} AS r ON r.rule_id = rsd.rule_id " .format(TABLE_RULES)
        sql += "JOIN {0} AS rk ON rk.rule_id = r.rule_id " .format(TABLE_RULE_KEYWORD)
        sql += "JOIN {0} AS k ON k.keyword_id = rk.keyword_id " .format(TABLE_KEYWORDS)
        sql += "JOIN {0} AS rf ON rf.rule_id = r.rule_id " .format(TABLE_RULE_FIELD)
        sql += "WHERE c.type LIKE '{0}' AND rf.field_id = {1} AND p.name LIKE '{2}' " .format(stage, field_id, parent_id)

        print sql
        self.cursor.execute(sql)

        rows = self.cursor.fetchall()

        results = []
        for row in rows:    # OPTIMIZE HERE, return directly in tuple format instead of a list
            results.append(row)

        return results
#MySQLUtils()._get_rule_subset_by_phase_and_field('Category 1', 1)
#MySQLUtils()._get_rule_subset_by_phase_and_field('Profile Type', 1)
#print MySQLUtils().get_rule_subset_by_phase_field_parent('Category 1', 1, "Financial Market Professionals")
