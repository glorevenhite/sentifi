from MySQLUtils import MySQLUtils
from Constant import *
from Rule import Rule

import simplejson
import numpy

import pprint



#All function return in json format
class Ruler(object):
    def __init__(self):
        self.connection = MySQLUtils().connection

    def get_rule_subset_by_phase_and_field(self, stage, field_id):
        list_rule_subset = MySQLUtils()._get_rule_subset_by_phase_and_field(stage,field_id)

        # Building json
        # FORMAT:
        # {cat_name1:
        #   {subset_id:{'exclusion':[n1,n2,n3], 'rules':{rid:[a1,b1],rid:[a2,b1]}},
        #    subset_id:{'exclusion':[m1,m2,m3], 'rules':{rid:[x1,y1], rid:[x1,y2}},
        #  cat_name2:
        #   {subset_id:{'exclusion':[n1,n2,n3], 'rules':{rid:[a1,b1],rid:[a2,b1]}},
        #    subset_id:{'exclusion':[m1,m2,m3], 'rules':{rid:[x1,y1], rid:[x1,y2}},
        # }
        dict_result = {}
        for item in list_rule_subset:

            class_name = item[0]
            subset_id = item[1]
            rule_id = item[2]
            word = item[3].encode('utf-8')
            status = item[4]    # inclusion or exclusion
            ss1 = {class_name: {}}
            if class_name not in dict_result.keys():
                #create new one
                dict_result.update({class_name: {subset_id: {'exclusion': [], 'rules': {rule_id: []}}}})

                if status == 0:     # Inclusion
                    dict_result.get(class_name).get(subset_id).get('rules').get(rule_id).append(word)
                else:
                    dict_result.get(class_name).get(subset_id).get('exclusion').append(word)
            else:
                #update
                if subset_id not in dict_result.get(class_name).keys():
                    # new subset_id. We going to add new subset
                    dict_result.get(class_name).update({subset_id: {'exclusion': [], 'rules': {rule_id: []}}})

                    #since current subset_id is fresh, rule_id absolutely is fresh too.
                    if status == 0:
                        dict_result.get(class_name).get(subset_id).get('rules').update({rule_id: [word]})
                    else:
                        dict_result.get(class_name).get(subset_id).get('exclusion').append(word)
                else:
                    #Update existed subset
                    # check rule_id
                    #print dict_result.get(class_name).get(subset_id).get('rules').keys()
                    if rule_id not in dict_result.get(class_name).get(subset_id).get('rules').keys():
                        if status == 0:
                            dict_result.get(class_name).get(subset_id).get('rules').update({rule_id: [word]})
                        else:
                            dict_result.get(class_name).get(subset_id).get('exclusion').append(word)
                    else:
                        #rule existed already

                        if status == 0:
                            lst = dict_result.get(class_name).get(subset_id).get('rules').get(rule_id)

                            dict_result.get(class_name).get(subset_id).get('rules').get(rule_id).append(word)
                        else:
                            dict_result.get(class_name).get(subset_id).get('exclusion').append(word)

        #pprint.pprint(dict_result)
        return dict_result

    def get_ruleset_by_phase(self, phase, field):
        sql = "SELECT DISTINCT c.type, c.name, r.rule_id, rk.keyword_id, k.keyword, field, rk.status "
        sql += "FROM {0} AS c " .format(TABLE_CATEGORIES)
        sql += "JOIN {0} AS r ON r.category_id = c.id " .format(TABLE_RULES)
        sql += "JOIN {0} AS rf ON rf.rule_id = r.rule_id " .format(TABLE_RULE_FIELD)
        sql += "JOIN {0} AS f ON rf.field_id = f.id " .format(TABLE_FIELDS)
        sql += "JOIN {0} AS rk ON r.rule_id = rk.rule_id " .format(TABLE_RULE_KEYWORD)
        sql += "JOIN {0} AS k ON rk.keyword_id = k.keyword_id " .format(TABLE_KEYWORDS)
        sql += "WHERE c.type LIKE '{0}' AND f.id = {1} " .format(phase, field)
        sql += "ORDER BY c.id, r.rule_id "

        cursor = self.connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results):
            return results
        else:
            return "None"

    def get_classes_by_phase_name(self, phase):
        sql = "SELECT c.category_id, c.name "
        sql += "FROM {0} AS c " .format(TABLE_CATEGORIES)
        sql += "WHERE LCASE(c.type) LIKE '{0}' " .format(phase.lower())

        cursor = self.connection.cursor()
        cursor.execute(sql)

        rows = cursor.fetchall()

        values = {}
        for row in rows:
            values.update({row[0]: row[1]})

        return {phase: values}

    def get_ruleset_in_json2(self, phase, field):
        #Get keywords for specific phase: Profile Type, Profile group, category 1, category 2
        rows = Ruler().get_ruleset_by_phase(phase, field)
        if len(rows) > 0:

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

                key = ruleset.keys()[0]
                values = ruleset.values()[0]
                list_ruleset.update({key: values})

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
                rule = self._make_rule_2(subset_rows)
                ruleset.append(rule)

        return ruleset

    def _make_json_ruleset(self, cat_name, list_rules):
        values = {}
        for rule in list_rules:
            dct = dict(rule.keywords_json_2())
            key = dct.keys()[0]
            value = dct.values()[0]
            values.update({key: value})

        json = {cat_name: values}
        return json

    # Making rule from subset of rows those having same RULE_ID.
    # We basically add up keywords to the based_word, and_words, not_words of rule depend on the status
    def _make_rule(self, list_rows):
        if len(list_rows) > 0:
            rule = Rule(list_rows[0][2])    # Rule id
            rule.set_category(list_rows[0][1])  # Category. i.e. Financial Analyst
            for row in list_rows:
                word = row[4]           # keywords
                status = int(row[6])    # status: based, and or not
                if status == 0:
                    rule.add_new_based_word(unicode(word).encode('utf-8'))
                elif status == 1:
                    rule.add_new_and_words(unicode(word).encode('utf-8'))
                elif status == 2:
                    rule.add_new_not_words(unicode(word).encode('utf-8'))
            return rule

    #We only care about inclusion and exclusion. Do not care about the based, and and not keywords anymore
    def _make_rule_2(self, list_rows):
        if len(list_rows) > 0:
            rule = Rule(list_rows[0][2])
            rule.set_category(list_rows[0][1])
            for row in list_rows:
                word = row[4]
                status = int(row[6])
                if status == 0:
                    rule.add_new_and_words(word)
                else:
                    rule.add_new_not_words(word)
            return rule

    def get_parent_phase(self, category_name):
        sql = "SELECT c.name FROM Categories AS c WHERE c.id IN (SELECT c.above_node_id "
        sql += "FROM Categories AS c "
        sql += "WHERE c.name = '{0}')" .format(category_name)

        print sql
        cursor = self.connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()

        for row in results:
            if row[0] != "Null":
                json_data = {category_name: row[0]}
                return simplejson.dumps(json_data)



#print Ruler().get_parent_phase('Financial Analyst')
#print Ruler().get_classes_by_phase_name('Category 1')
#Ruler().get_rule_subset_by_phase_and_field('Category 1', 1)