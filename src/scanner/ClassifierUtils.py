from MySQLUtils import MySQLUtils
from Constant import SQLTableName

class ClassifierUtils(object):
    def _get_fields(self):
        list_column_names = ['id','field']
        table_name = 'tbl_applied_field'
        results = MySQLUtils().select(list_column_names, table_name)

        dict_results = {}
        for item in results:
            dict_results.update({item[0]:item[1]})

        return dict_results

    #MAIN
    def get_list_ruleset_given_phase(self, phase_name):

        list_cat_ids_in_phase = self._get_list_cat_id_given_phase(phase_name)
        print list_cat_ids_in_phase

        dict_results = {}
        for cat_id in list_cat_ids_in_phase:
            #key = self._get_category_name_given_cat_id(cat_id)key = self._get_category_name_given_cat_id(cat_id)
            #values =
            ruleset = self.get_ruleset_for_given_category_id(cat_id)
            dict_results.update({ruleset.keys()[0]:ruleset.values()[0]})

        print dict_results
        return dict_results



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

        list_rule_ids = MySQLUtils().select_where(list_column_names, table_name, list_where_clauses)


        values = []
        for rule_id in list_rule_ids:
            values.append(self._get_keywords_for_given_rule_id(rule_id))

        ruleset = {}
        key = self._get_category_name_given_cat_id(cat_id)
        ruleset.update({key:values})

        return ruleset

    #Get keywords given by rule_id
    def _get_keywords_for_given_rule_id(self, rule_id):
        query  = "SELECT k.keyword_id, k.keyword "
        query += "FROM %s AS k " %SQLTableName().KEYWORDS
        query += "JOIN %s AS rk " %SQLTableName().RULE_KEYWORD
        query += "ON k.keyword_id = rk.keyword_id "
        query += "WHERE rk.rule_id = %s " %str(rule_id)


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


#print ClassifierUtils()._get_fields()
#print ClassifierUtils().get_ruleset_for_given_category_id(46)

#print ClassifierUtils()._get_keywords_for_given_rule_id(117)
#ClassifierUtils()._get_list_cat_id_given_phase("'Category 1'")
ClassifierUtils().get_list_ruleset_given_phase("'Category 1'")

