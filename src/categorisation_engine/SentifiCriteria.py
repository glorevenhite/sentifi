from Rule import Rule

class SentifiCriteria(object):
    def __init__(self, json_data):
        self.phase = json_data['phase']
        self.channel = json_data['channel']
        self.field = json_data['field']
        self.rule_id = json_data['rule_id']
        self.based_words = json_data['based']
        self.and_words = json_data['and']
        self.not_words = json_data['not']

    def get_rules(self):

        list_rules = []

        for bw in self.based_words:
            rule = Rule()
            if len(self.and_words) == 0:
                rule.inc_keywords = [bw]
                list_rules.append(rule)

            for aw in self.and_words:
                rule.inc_keywords = [bw, aw]

                if len(self.not_words) == 0:
                    rule.exc_keywords = []
                for nw in self.not_words:
                    rule.exc_keywords = [nw]
                list_rules.append(rule)


json_data = {'phase': 'category 2', 'channel': 'twitter', 'field': 'name', 'rule_id': '1', 'based': ['columnist', 'journalist'], 'and':['humanist'], 'not': ['photo']}

c = SentifiCriteria(json_data)
print c.based_words