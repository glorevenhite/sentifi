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
            if len(query.not_words):
                self.exclusion.extend(query.not_words)
        return self.exclusion

    def get_rules(self):
        list_rules = []

        for query in self.queries:
            rules = query.get_list_simple_rules()
            list_rules.extend(rules)

        return list_rules