from MySQLUtils import MySQLUtils
from Constant import *


class Ruler(object):
    def __init__(self):
        self.connection = MySQLUtils().connection

    @staticmethod
    def get_rules(stage_name, field_name, class_name):
        list_rules = MySQLUtils().get_rule_subset_by_phase_field_parent(stage_name, field_name, class_name)

        return {class_name: list_rules}

    def get_classes(self, phase, parent_name):
        sql = "SELECT c.category_id, c.name, p.name "
        sql += "FROM {0} AS c " .format(TABLE_CATEGORIES)
        sql += "JOIN {0} as p ON p.category_id = c.parent_cat_id " .format(TABLE_CATEGORIES)
        sql += "WHERE LCASE(c.type) LIKE '{0}' AND p.name LIKE '{1}' " .format(phase.lower(), parent_name)

        cursor = self.connection.cursor()
        cursor.execute(sql)

        rows = cursor.fetchall()

        values = {}
        for row in rows:
            values.update({row[0]: row[1]})

        return {phase: values}

    def get_parent_phase(self, category_name):
        sql = "SELECT c.name "
        sql += "FROM {0} AS c WHERE c.category_id IN (SELECT c.parent_cat_id " .format(TABLE_CATEGORIES)
        sql += "FROM {0} AS c " .format(TABLE_CATEGORIES)
        sql += "WHERE c.name = '{0}')" .format(category_name)

        cursor = self.connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchone()

        #for row in results:
        #    if row[0] != "Null":
        #        json_data = {category_name: row[0]}
        #        return json_data

        return results[0]

print Ruler().get_parent_phase('Architecture, Construction & Design')
#print Ruler().get_classes_by_phase_name('Publisher Group', 'O')
#Ruler().get_rule_subset_by_phase_and_field('Category 1', 1)