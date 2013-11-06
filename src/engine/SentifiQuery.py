__author__ = 'vinh.vo@sentifi.com'

import itertools


class SentifiQuery(object):
    def __init__(self):
        self.id = ""
        self.based_words = []
        self.and1_words = []
        self.and2_words = []
        self.not_words = []

    def get_list_simple_rules(self):
        if self.based_words and self.and1_words and self.and2_words:
            return list(itertools.product(self.based_words, self.and1_words, self.and2_words))

        if len(self.and2_words) == 0 and self.and1_words:
            return list(itertools.product(self.based_words, self.and1_words))

        return list(self.based_words)


if __name__ == "__main__":
    query = SentifiQuery()
    query.based_words = [1, 2]
    query.and1_words = [3, 4]
    query.and2_words = [5, 6]
    #print query.get_list_simple_rules()


