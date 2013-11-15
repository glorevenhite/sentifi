from MySQLUtils import MySQLUtils
from Constant import *
from Switcher import *
from Rule import *


class Ruler(object):
    def __init__(self):
        self.category = [
                         Profile().PER,
                         Profile().ORG,
                         ]
    def load_all_ruleset(self, category):
        index = self.category.index(category)
        return Switcher[index]()

    # Each list_rulesets contain collection of rulesets. Each ruleset identify the Category (Class) of given field
    def load_list_rulesets(self, field, step):
        if (step == 'PT'):
            if (field == 'FN'):
                list_rulesets = []

                #Loading rulset for identification of Person on Fullname
                connection = MySQLUtils().connection
                cursor = connection.cursor()
                cursor.execute("SELECT tbl_rule.rule_id FROM tbl_rule")
                list_rulesets.append(None)

                ruleset1 = [None]*8
                ruleset1[0] = Rule(['.com'], [])
                ruleset1[1] = Rule(['bank'], [])
                ruleset1[2] = Rule(['market'], [])
                ruleset1[3] = Rule(['ltd'], [])
                ruleset1[4] = Rule(['limited'], [])
                ruleset1[5] = Rule(['bv'], [])
                ruleset1[6] = Rule(['llc'], [])
                ruleset1[7] = Rule(['news'], [])

                list_rulesets.append(ruleset1)
                return list_rulesets
            else:
                #load ruleset for description
                ruleset1 = [None]*7
                ruleset1[0] = Rule(['believer'], [])
                ruleset1[1] = Rule(['consultant'], [])
                ruleset1[2] = Rule(['i'], [])
                ruleset1[3] = Rule(['my'], [])
                ruleset1[4] = Rule(['owner'], [])
                ruleset1[5] = Rule(['student'], [])
                ruleset1[6] = Rule(['financial-analyst'], []) #extent example for test

                ruleset2 = [None]*3
                ruleset2[0] = Rule(['we'],[])
                ruleset2[1] = Rule(['our'],[])
                ruleset2[2] = Rule(['provider'],[])

                list_ruleset = []
                list_ruleset.append(ruleset1)
                list_ruleset.append(ruleset2)
                return list_ruleset
        elif (step == 'C2'):
            pass
        else:
            pass

    def _load_rule_for_given_category(self, cat_id):
        connection = MySQLUtils().connection
        cursor = connection.cursor()
        sql =  "SELECT  c.name, r.rule_id, rk.keyword_id, k.keyword "
        sql += "FROM tbl_rule AS r "
        sql += "JOIN tbl_category AS c ON r.category_id = c.id "
        sql += "JOIN tbl_rule_keyword AS rk ON r.rule_id = rk.rule_id "
        sql += "JOIN tb_keyword AS k ON k.keyword_id = rk.keyword_id "
        sql += "WHERE c.id = %s AND r.type_not = 0"  %cat_id

        cursor.execute(sql)
        rows = cursor.fetchall()

        dict_result = {}
        for row in rows:
            dict_result.update({row[1]:row[3]})

        return dict_result

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
#Ruler()._load_rule_for_given_category(45)

#print Ruler()._load_all_category1_name()

Ruler()._load_rulesets()

#print Ruler().load_all_ruleset('ORGANISATION')