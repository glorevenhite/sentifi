from MySQLUtils import MySQLUtils
from Constant import *
import simplejson
from StringIO import StringIO

#All function return in json format
class Ruler(object):
    def __init__(self):
        self.connection = MySQLUtils().connection

    def get_list_category_names_by_phase(self, phase):
        cursor = self.connection.cursor()
        sql = "SELECT c.name "
        sql += "FROM {0} AS c " .format(TABLE_CATEGORIES)
        sql += "WHERE UCASE(c.type) = '{0}' " .format(phase)

        cursor.execute(sql)
        rows = cursor.fetchall()

        list_categories = []
        for row in rows:
            list_categories.append(row[0])

        dict_result = {phase: list_categories}

        #Return a string of json
        return simplejson.dumps(dict_result)

    def get_list_category_ids_by_phase(self, phase):
        cursor = self.connection.cursor()
        sql = "SELECT c.id, c.name "
        sql += "FROM {0} AS c " .format(TABLE_CATEGORIES)
        sql += "WHERE UCASE(c.type) = '{0}' " .format(phase)

        cursor.execute(sql)
        rows = cursor.fetchall()

        list_categories = []
        for row in rows:
            dict_value = {}
            dict_value.update({row[0]: row[1]})
            list_categories.append(dict_value)

        dict_result = {phase: list_categories}

        #Return a string of json
        return simplejson.dumps(dict_result)

    def get_list_rules_for_by_category_name(self, cat_name, field_id):
        cursor = self.connection.cursor()

        sql = "SELECT r.rule_id, k.keyword "
        sql += "FROM %s AS r " % TABLE_RULE_CATEGORY
        sql += "JOIN %s AS c ON r.category_id = c.id " % TABLE_CATEGORIES
        sql += "JOIN %s AS rk ON r.rule_id = rk.rule_id " % TABLE_RULE_KEYWORD
        sql += "JOIN %s AS k ON k.keyword_id = rk.keyword_id " % TABLE_KEYWORDS
        sql += "JOIN %s AS rf ON r.rule_id = rf.rule_id " % TABLE_RULE_FIELD
        sql += "WHERE c.name LIKE '{0}' AND r.type_not = 0 AND rf.field_id = {1}" .format(cat_name, field_id)

        print sql

        cursor.execute(sql)
        rows = cursor.fetchall()

        dict_values = {}
        for row in rows:
            dict_values.update({row[0]: row[1]})

        #using category name as key
        dict_key = cat_name.encode('utf-8')

        dict_results = {dict_key: dict_values}

        return simplejson.dumps(dict_results)

    def get_list_rules_by_category_id(self, cat_id, field_id):
        cursor = self.connection.cursor()

        sql = "SELECT DISTINCT r.rule_id "
        sql += "FROM %s AS r " % TABLE_RULE_CATEGORY
        sql += "JOIN %s AS c ON r.category_id = c.id " % TABLE_CATEGORIES
        sql += "JOIN %s AS rf ON r.rule_id = rf.rule_id " % TABLE_RULE_FIELD
        sql += "WHERE c.id = {0} AND r.type_not = 0" .format(cat_id, field_id)

        cursor.execute(sql)
        rows = cursor.fetchall()

        list_values = []
        for row in rows:
            list_values.append(row[0])

        #using category name as key
        dict_key = cat_id

        dict_results = {dict_key: list_values}

        return simplejson.dumps(dict_results)

    def get_rules(self, rule_id):
        based_keywords = self.get_based_keywords_by_rule_id(rule_id, 0)
        and_keywords = self.get_based_keywords_by_rule_id(rule_id, 1)
        not_keywords = self.get_based_keywords_by_rule_id(rule_id, 2)

        str_json = {rule_id: {'based': based_keywords, 'and': and_keywords, 'not': not_keywords}}

        return simplejson.dumps(str_json)

    def get_based_keywords_by_rule_id(self, rule_id, keyword_type):
        cursor = self.connection.cursor()

        sql = "SELECT r.rule_id, k.keyword "
        sql += "FROM %s AS r " % TABLE_RULE_CATEGORY
        sql += "JOIN %s AS rk ON r.rule_id = rk.rule_id " % TABLE_RULE_KEYWORD
        sql += "JOIN %s AS k ON rk.keyword_id = k.keyword_id " % TABLE_KEYWORDS
        sql += "WHERE r.rule_id = {0} AND r.type_not = 0 AND rk.status = {1} " .format(rule_id, keyword_type)

        print sql
        cursor.execute(sql)
        rows = cursor.fetchall()

        list_values = []
        for row in rows:
            list_values.append(row[1])

        return simplejson.dumps(list_values)


    def get_list_rules_for_by_category_id(self, cat_id, field_id):
        cursor = self.connection.cursor()

        sql = "SELECT r.rule_id, k.keyword "
        sql += "FROM %s AS r " % TABLE_RULE_CATEGORY
        sql += "LEFT JOIN %s AS c ON r.category_id = c.id " % TABLE_CATEGORIES
        sql += "LEFT JOIN %s AS rk ON r.rule_id = rk.rule_id " % TABLE_RULE_KEYWORD
        sql += "LEFT JOIN %s AS k ON k.keyword_id = rk.keyword_id " % TABLE_KEYWORDS
        sql += "LEFT JOIN %s AS rf ON r.rule_id = rf.rule_id " % TABLE_RULE_FIELD
        sql += "WHERE c.id = {0} AND r.type_not = 0" .format(cat_id, field_id)

        cursor.execute(sql)
        rows = cursor.fetchall()

        list_values = []
        for row in rows:
            dict_value = {}
            print row[1]
            dict_value.update({row[0]: unicode(row[1]).encode('utf-8', errors='strict')})
            list_values.append(dict_value)

        #using category name as key
        dict_key = cat_id

        dict_results = {dict_key: list_values}

        return simplejson.dumps(dict_results)

    def _get_category_name_by_id(self, cat_id):
        cursor = self.connection.cursor()

        sql = "SELECT name "
        sql += "FROM %s " % TABLE_CATEGORIES
        sql += "WHERE id = %s " % cat_id

        cursor.execute(sql)

        result = cursor.fetchone()

        return result[0]

#Ruler().get_list_rules_for_by_category_name('Financial Analyst', 1)
#Ruler().get_list_rules_for_by_category_id(45,1)
#print Ruler().get_list_rules_by_category_id(45,1)
#print Ruler().get_based_keywords_by_rule_id(15)
#json_data = simplejson.loads(Ruler().get_rules(15))

#print json_data['15']['based']