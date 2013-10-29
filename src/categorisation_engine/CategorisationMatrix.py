__author__ = 'vinh.vo@sentifi.com'
import numpy


class CategorisationMatrix(object):
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = numpy.zeros((len(rows), len(cols)))

    def increase_by(self, field_name, class_name, increasing_value):
        x = self._get_col_pos(class_name)
        y = self._get_row_pos(field_name)
        self.matrix[x][y] += increasing_value

    def _get_row_pos(self, value):
        return self.rows.index(value)

    def _get_col_pos(self, value):
        return self.cols.index(value)

    def display(self):
        print self.matrix


rows = ['a','b']
cols = ['x','y','z']
matrix = CategorisationMatrix(rows, cols)

