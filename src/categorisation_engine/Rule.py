from SentifiWordsBank import  SentifiWordsBank
import simplejson

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
        print "Ruleset name:", self.rule_set_name
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