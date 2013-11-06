__author__ = 'vinh.vo@sentifi.com'


class SentifiCategory(object):
    def __init__(self):
        self.id = ""
        self.name = ""
        self.parent = ""
        self.exclusion = []
        self.inclusion = []
        self.queries = []

    def get_exclusion(self):
        for query in self.queries:
            self.exclusion.append(query.not_words)

    def get_rules(self):
        list_rules = []

        for query in self.queries:
            rules = query.get_list_simple_rules()
            list_rules.extend(rules)

        return list_rules