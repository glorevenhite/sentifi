__author__ = 'vinh.vo@sentifi.com'

from MySQLUtils import MySQLUtils


class Ruler():
    def __init__(self):
        self.connection = MySQLUtils().connection

    def get_category_name(self, stage, parent, field):
        sql = "SELECT * FROM {0} AS c " .format(TABLE_CATEGORIES)
        sql += "JOIN {0} AS q ON c.category_id = q.category_id " .format(TABLE_QUERIES)
        sql += "  "
