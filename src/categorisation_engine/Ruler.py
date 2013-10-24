from MySQLUtils import MySQLUtils
from Constant import *


class Ruler(object):

    def _load_list_rules_for_given_category(self, cat_id):
        connection = MySQLUtils().connection
        cursor = connection.cursor()
        sql = "SELECT  c.name, r.rule_id, rk.keyword_id, k.keyword "
        sql += "FROM %s AS r " % TABLE_RULE_CATEGORY
        sql += "JOIN %s AS c ON r.category_id = c.id " % TABLE_CATEGORIES
        sql += "JOIN %s AS rk ON r.rule_id = rk.rule_id " % TABLE_RULE_KEYWORD
        sql += "JOIN %s AS k ON k.keyword_id = rk.keyword_id " % TABLE_KEYWORDS
        sql += "WHERE c.id = %s AND r.type_not = 0" % cat_id

        cursor.execute(sql)
        rows = cursor.fetchall()

        dict_values = {}
        for row in rows:
            dict_values.update({row[1]: row[3]})

        dict_key = rows[0][0]

        dict_results = {dict_key: dict_values}

        return dict_results

    def _load_all_category1_name(self):
        connection = MySQLUtils().connection
        cursor = connection.cursor()
        sql =  "SELECT  c.id, c.name "
        sql += "FROM tbl_category AS c "
        sql += "WHERE c.type = 'Category 1' "

        cursor.execute(sql)
        rows = cursor.fetchall()

        #buiding dictionary type
        dict_results = {}
        for row in rows:
            dict_results.update({row[0]:row[1]})

        if dict_results is not None:
            return dict_results
        else:
            return None

    def _load_rulesets(self):
        dict_category1 = self._load_all_category1_name()
        cat_ids = dict_category1.keys()

        dict_results = {}
        for id in cat_ids:
            dict_results.update({dict_category1[id]:self._load_rule_for_given_category(id)})

            #list_results.append(self._load_rule_for_given_category(id))

        #print dict_results


        #for k in sorted(dict_results, key=lambda k:len(dict_results[k]), reverse=True):
         #   print k

#Loading rulset for identification of Person on Fullname
print Ruler()._load_list_rules_for_given_category(45)

#print Ruler()._load_all_category1_name()

#Ruler()._load_rulesets()

#print Ruler().load_all_ruleset('ORGANISATION')