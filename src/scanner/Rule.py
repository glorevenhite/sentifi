class Rule(object):
    def __init__(self, inclusion_list, exclusion_list ):
        self._inc = inclusion_list
        self._exc = exclusion_list
        self.keywords = self._inc + self._exc
        self.inc_keywords = set(inclusion_list)
        self.exc_keywords = set(exclusion_list)

    def display(self):
        print "Inclusion:"
        for kw in self._inc:
            print kw
        print "Exclusion:"
        for kw in self._exc:
            print kw
        print '-----------------'

"""For testing only"""
#rule = Rule(['financial', 'analyst'], ['trader'])
#print rule.keywords