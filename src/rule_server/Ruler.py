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
        sql = "SELECT  c.name "
        sql += "FROM tbl_category AS c "
        sql += "WHERE UCASE(c.type) = '{0}' " .format(phase)

        cursor.execute(sql)
        rows = cursor.fetchall()

        list_categories = []
        for row in rows:
            list_categories.append(row[0])

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

        cursor.execute(sql)
        rows = cursor.fetchall()

        list_keywords = []
        for row in rows:
            list_keywords.append(row[1])

        #using category name as key
        dict_key = cat_name

        dict_results = {dict_key: list_keywords}

        return simplejson.dumps(str(dict_results))

    def load_list_rules_for_by_category_id(self, cat_id, field_id):
        cursor = self.connection.cursor()

        sql = "SELECT r.rule_id, k.keyword "
        sql += "FROM %s AS r " % TABLE_RULE_CATEGORY
        sql += "JOIN %s AS c ON r.category_id = c.id " % TABLE_CATEGORIES
        sql += "JOIN %s AS rk ON r.rule_id = rk.rule_id " % TABLE_RULE_KEYWORD
        sql += "JOIN %s AS k ON k.keyword_id = rk.keyword_id " % TABLE_KEYWORDS
        sql += "JOIN %s AS rf ON r.rule_id = rf.rule_id " % TABLE_RULE_FIELD
        sql += "WHERE c.id = {0} AND r.type_not = 0" .format(cat_id, field_id)

        cursor.execute(sql)
        rows = cursor.fetchall()

        dict_values = {}
        for row in rows:
            dict_values.update({row[0]: row[1]})

        #using category name as key
        dict_key = self._get_category_name_by_id(cat_id)

        dict_results = {dict_key: dict_values}

        return dict_results

    def _get_category_name_by_id(self, cat_id):
        cursor = self.connection.cursor()

        sql = "SELECT name "
        sql += "FROM %s " % TABLE_CATEGORIES
        sql += "WHERE id = %s " % cat_id

        cursor.execute(sql)

        result = cursor.fetchone()

        return result[0]