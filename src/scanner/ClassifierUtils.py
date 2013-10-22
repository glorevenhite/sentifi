from MySQLUtils import MySQLUtils
from Constant import SQLTableName
import pprint
import json
from IOUtils import IOUtils

class ClassifierUtils(object):

    #MAIN
    def get_list_ruleset_given_phase(self, phase_name):

        #Retrieve the list of cat_id to which profiles will be classified to
        list_cat_ids_in_phase = self._get_list_cat_id_given_phase(phase_name)

        dict_results = {}
        for cat_id in list_cat_ids_in_phase:

            #get ruleset for given category. The result is dictionary type already
            ruleset = self.get_ruleset_for_given_category_id(cat_id)

            #update to dict_results
            dict_results.update({ruleset.keys()[0]:ruleset.values()[0]})
        dict = {}
        dict.update({phase_name.replace("'",""):dict_results})

        return dict

    #Get list CAT_ID for given PHASE
    def _get_list_cat_id_given_phase(self, phase_name):
        list_column_names = ['id']
        table_name = SQLTableName().CATEGORIES
        list_where_clauses = ['type', phase_name]

        list_category_ids = MySQLUtils().select_where(list_column_names, table_name, list_where_clauses)

        return list_category_ids

    def get_ruleset_for_given_category_id(self, cat_id):
        list_column_names = ['rule_id']
        table_name = SQLTableName().RULE_CATEGORY
        list_where_clauses = ['category_id', str(cat_id)]

        #get list of RULE_IDS
        list_rule_ids = MySQLUtils().select_where(list_column_names, table_name, list_where_clauses)


        values1 = []    #Values for dictionary
        for rule_id in list_rule_ids:
            values1.append(self._get_included_keywords_for_given_rule_id(rule_id))

        dict1 = {}
        dict1 = {'inclusion':values1}

        values2 = []
        for rule_id in list_rule_ids:
            values2.append(self._get_excluded_keywords_for_given_rule_id(rule_id))

        dict2 = {}
        dict2 = {'exclusion':values2}

        ruleset = {}
        values = [dict1, dict2]
        key = self._get_category_name_given_cat_id(cat_id)

        ruleset[key] = values

        return ruleset

    #Get keywords given by rule_id
    def _get_keywords_for_given_rule_id(self, rule_id):
        query  = "SELECT k.keyword_id, k.keyword "
        query += "FROM %s AS k " %SQLTableName().KEYWORDS
        query += "JOIN %s AS rk " %SQLTableName().RULE_KEYWORD
        query += "ON k.keyword_id = rk.keyword_id "
        query += "JOIN %s AS rc " %SQLTableName().RULE_CATEGORY
        query += "ON rc.rule_id = rk.rule_id "
        query += "WHERE rk.rule_id = %s " %str(rule_id)


        rows = MySQLUtils().select_query(query)

        dict_results = {}
        for row in rows:
            dict_results.update({str(row[0]):row[1]})

        return dict_results

    def _get_included_keywords_for_given_rule_id(self, rule_id):
        query  = "SELECT k.keyword_id, k.keyword "
        query += "FROM %s AS k " %SQLTableName().KEYWORDS
        query += "JOIN %s AS rk " %SQLTableName().RULE_KEYWORD
        query += "ON k.keyword_id = rk.keyword_id "
        query += "JOIN %s AS rc " %SQLTableName().RULE_CATEGORY
        query += "ON rc.rule_id = rk.rule_id "
        query += "WHERE rk.rule_id = %s AND rc.type_not = 0" %str(rule_id)


        rows = MySQLUtils().select_query(query)

        dict_results = {}
        for row in rows:
            dict_results.update({str(row[0]):row[1]})

        return dict_results

    def _get_excluded_keywords_for_given_rule_id(self, rule_id):
        query  = "SELECT k.keyword_id, k.keyword "
        query += "FROM %s AS k " %SQLTableName().KEYWORDS
        query += "JOIN %s AS rk " %SQLTableName().RULE_KEYWORD
        query += "ON k.keyword_id = rk.keyword_id "
        query += "JOIN %s AS rc " %SQLTableName().RULE_CATEGORY
        query += "ON rc.rule_id = rk.rule_id "
        query += "WHERE rk.rule_id = %s AND rc.type_not = 1" %str(rule_id)


        rows = MySQLUtils().select_query(query)

        dict_results = {}
        for row in rows:
            dict_results.update({str(row[0]):row[1]})

        return dict_results

    #Get Name of Category given by category_id
    def _get_category_name_given_cat_id(self, cat_id):
        list_column_names = ['name']
        table_name = SQLTableName().CATEGORIES
        list_where_clauses = ['id', str(cat_id)]
        results = MySQLUtils().select_where(list_column_names, table_name, list_where_clauses)

        return results[0]

    #Retrieving fields
    def _get_fields(self):
        list_column_names = ['id','field']
        table_name = 'tbl_applied_field'
        results = MySQLUtils().select(list_column_names, table_name)

        dict_results = {}
        for item in results:
            dict_results.update({item[0]:item[1]})

        return dict_results


#print ClassifierUtils()._get_fields()
#print ClassifierUtils().get_ruleset_for_given_category_id(46)

#print ClassifierUtils()._get_keywords_for_given_rule_id(117)
#ClassifierUtils()._get_list_cat_id_given_phase("'Category 1'")
dict_ruleset = (ClassifierUtils().get_list_ruleset_given_phase("'Profile Type'"))
#pprint.pprint(dict_ruleset)
print dict_ruleset['Profile Type']
print dict_ruleset['Profile Type']['P'][1]
#print dict_ruleset['Profile Type']['P'][1]['exclusion'][0]

str = json.dumps(dict_ruleset)
print str
#IOUtils().save_json_data_to_file(str, "result.json", "D:\\")


