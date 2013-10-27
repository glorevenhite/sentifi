from MySQLUtils import MySQLUtils
from Constant import *
from Rule import Rule

import simplejson
import numpy
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
        dict_key = cat_name

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

    def get_ruleset_by_phase(self, phase):
        sql = "SELECT DISTINCT c.type, c.name, r.rule_id, rk.keyword_id, k.keyword, field, rk.status "
        sql += "FROM {0} AS c " .format(TABLE_CATEGORIES)
        sql += "JOIN {0} AS r ON r.category_id = c.id " .format(TABLE_RULE_CATEGORY)
        sql += "JOIN {0} AS rf ON rf.rule_id = r.rule_id " .format(TABLE_RULE_FIELD)
        sql += "JOIN {0} AS f ON rf.field_id = f.id " .format(TABLE_FIELDS)
        sql += "JOIN {0} AS rk ON r.rule_id = rk.rule_id " .format(TABLE_RULE_KEYWORD)
        sql += "JOIN {0} AS k ON rk.keyword_id = k.keyword_id " .format(TABLE_KEYWORDS)
        sql += "WHERE c.type LIKE '{0}' " .format(phase)
        sql += "ORDER BY c.id, r.rule_id "

        cursor = self.connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()

        return results

    def get_ruleset_in_json(self):
        #Get keywords for specific phase: Profile Type, Profile group, category 1, category 2
        rows = Ruler().get_ruleset_by_phase('Category 1')

        result = {}
        for row in rows:

            super_key = row[0]  # Type, i.e, Profile Type, Profile Group, Category 1, Category 2
            if result == {}:
                result.update({super_key: {}})

            main_key = row[1]   # i.e., financial analyst, portfolio manager
            if main_key not in result[super_key].keys():
                result.get(super_key).update({main_key: {}})

            sub_key = int(row[2])    #rule id
            if sub_key not in result[super_key][main_key].keys():
                keyword = row[4]
                status = row[6]

                if status == 0:
                    based_words = {'based': [keyword]}
                    status = {'status': based_words}
                    result.get(super_key).get(main_key).update({sub_key: status})
                    #result.[super_key][main_key].update({sub_key: {'status': [{based_words}]}})
                elif status == 1:
                    and_words = {'and': [keyword]}
                    result[super_key][main_key].update({sub_key: {'status': {[based_words,and_words]}}})
                elif status == 2:
                    not_words = {'not': [keyword]}
                    result[super_key][main_key].update({sub_key: {'status': {[based_words,and_words, not_words]}}})
            else:
                value = row[4]
                status = row[6]
                if status == 0:
                    d = result.get(super_key).get(main_key).get(sub_key).get('status').get('based')
                    d.append(value)
                    result.get(super_key).get(main_key).get(sub_key).get('status').update({'status': d})

        return result

    def get_ruleset_in_json2(self, phase):
        #Get keywords for specific phase: Profile Type, Profile group, category 1, category 2
        rows = Ruler().get_ruleset_by_phase(phase)

        arr = numpy.array(rows)

        #Get list of category name by select only the 2nd-column from array
        list_category_name = set(arr[:, 1])

        list_ruleset = {}

        for cat_name in list_category_name:
            rs = []
            subset_rows = arr[arr[:, 1] == str(cat_name)]
            rs.append(subset_rows)
            list_rules = self._make_ruleset(subset_rows)

            #json format
            ruleset = self._make_json_ruleset(cat_name, list_rules)
            #list_ruleset.append(ruleset)

            key = ruleset.keys()[0]
            values = ruleset.values()[0]
            list_ruleset.update({key:values})
        results = {}
        results.update({phase: list_ruleset})


        return simplejson.dumps(results)

    def _make_ruleset(self, list_rows):
        category_name = list_rows[0][1]
        list_rule_ids = set(list_rows[:, 2])
        ruleset = []
        if len(list_rows) > 0:
            for id in list_rule_ids:
                subset_rows = list_rows[list_rows[:, 2] == str(id)]
                rule = self._make_rule(subset_rows)
                ruleset.append(rule)

        return ruleset

    def _make_json_ruleset(self, cat_name, list_rules):
        values = {}
        for rule in list_rules:
            dct = dict(rule.keywords_json())
            key = dct.keys()[0]
            value = dct.values()[0]
            values.update({key: value})

        json = {cat_name: values}
        return json

    # Making rule from subset of rows those having same RULE_ID.
    # We basically add up keywords to the based_word, and_words, not_words of rule depend on the status
    def _make_rule(self, list_rows):
        if len(list_rows) > 0:
            rule = Rule(list_rows[0][2])
            rule.set_category(list_rows[0][1])
            for row in list_rows:
                word = row[4]
                status = int(row[6])
                if status == 0:
                    rule.add_new_based_word(word)
                elif status == 1:
                    rule.add_new_and_words(word)
                elif status == 2:
                    rule.add_new_not_words(word)
            return rule

ruleset = Ruler().get_ruleset_in_json2(phase = 'Profile Type')
print ruleset


