from SentifiWordsBank import  SentifiWordsBank
import simplejson
import itertools


class ComplexRule(object):
    def __init__(self, name, json_data):
        self.name = name

        based = simplejson.loads(json_data['based'])
        and_keywords = simplejson.loads(json_data['and'])
        not_keywords = simplejson.loads(json_data['not'])


        list_rules = []
        for bw in based:
            if len(and_keywords) > 0:
                for aw in and_keywords:
                    rule = Rule()
                    rule.rule_set_name = self.name
                    rule.inc_keywords = [bw, aw]
                    if len(not_keywords) > 0:
                        for nw in not_keywords:
                            rule.exc_keywords = [nw]
                    else:
                        rule.exc_keywords = []
                    list_rules.append(rule)
            else:
                if len(not_keywords) > 0:
                    for nw in not_keywords:
                        rule = Rule()
                        rule.rule_set_name = self.name
                        rule.inc_keywords = [bw]
                        rule.exc_keywords = [nw]
                        list_rules.append(rule)

        print len(list_rules)
        self.rules = list_rules

class Rule(object):
    def __init__(self):
        self.rule_set_name = ""
        self.inc_keywords = []
        self.exc_keywords = []
        self.keywords = []

    def get_inclusion(self):
        #lowercase and strip any space in both left and right side
        return [word.lower().strip().replace(" ", "-") for word in self.inc_keywords]

    def get_exclusion(self):
        #lowercase and strip any space in both left and right side
        return [word.lower().strip() for word in self.exc_keywords]

    def get_wordsbank(self):
        list_words = self.inc_keywords + self.exc_keywords
        return self._build_wordsbank(list_words)

    def _build_wordsbank(self, list_words):
        return SentifiWordsBank().build_sorted_dictionary(list_words)

    def display(self):
        print "Inclusion:"
        for kw in self.inc_keywords:
            print kw
        print "Exclusion:"
        for kw in self.exc_keywords:
            print kw
        print '-----------------'

"""For testing only"""
#rule = Rule(['financial', 'analyst'], ['trader'])
#print rule.keywords