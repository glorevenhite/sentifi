class RuleSet(object):
    def __init__(self, json_data):
        self.rules = self._get_rules_from_json(json_data)

    def display(self):
        print "Inclusion:"
        for kw in self._inc:
            print kw
        print "Exclusion:"
        for kw in self._exc:
            print kw
        print '-----------------'

    def _get_rules_from_json(self, json_data):
        #format json
        json_data = {}

        rules = []




        return rules

    def _load_rules_from_database(self):
        pass

#format json

"""For testing only"""
#rule = Rule(['financial', 'analyst'], ['trader'])
#print rule.keywords