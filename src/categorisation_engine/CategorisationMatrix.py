__author__ = 'vinh.vo@sentifi.com'
import numpy


class CategorisationMatrix(object):
    def __init__(self, rows, cols):
        self.rows = sorted(rows)
        self.cols = sorted(cols)
        self.matrix = numpy.zeros((len(rows), len(cols)))

    def get_matrix(self):
        return self.matrix

    def increase_by(self, field_name, class_name, increasing_value):
        x = self._get_col_pos(class_name)
        y = self._get_row_pos(field_name)
        self.matrix[y][x] += increasing_value

    def _get_row_pos(self, value):
        return self.rows.index(value)

    def _get_col_pos(self, value):
        return self.cols.index(value)

    def get_class_name(self):
        arr = numpy.array(self.matrix)
        sum_array = arr.sum(axis=0)
        max_index = sum_array.argmax()

        class_name = self.cols[max_index]

        return class_name

    def display(self):
        #print self.get_class_name()
        print "MATRIX:"
        print self.matrix