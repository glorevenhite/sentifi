__author__ = 'vinh.vo@sentifi.com'


class RuleSet(object):
    def __init__(self):
        self.cat_name = ""
        self.exclusion = []
        self.rules = []

    def display(self):
        print self.cat_name, ":", self.exclusion, ":", self.rules
