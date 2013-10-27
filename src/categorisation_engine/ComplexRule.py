import itertools
from Rule import Rule


class ComplexRule(object):
    def __init__(self, name, rule_id, json_data):
        self.name = name
        self.rule_id = rule_id
        based_keywords = json_data[rule_id]['status']['based']
        and_keywords = json_data[rule_id]['status']['and']
        not_keywords = json_data[rule_id]['status']['not']

        list_rules = self._make_rules(based_keywords, and_keywords, not_keywords)

        self.rules = list_rules

    def _make_rules(self, bws, aws, nws):
        list_rules = []
        if len(bws) > 0:
            if len(aws) > 0:
                if len(nws) > 0:
                    prod_list = list(itertools.product(bws, aws, nws))
                    for item in prod_list:
                        rule = Rule()
                        rule.rule_set_name = self.name
                        rule.inc_keywords = [item[0], item[1]]
                        rule.exc_keywords = [item[2]]
                        list_rules.append(rule)
                else:
                    prod_list = list(itertools.product(bws, aws))
                    for item in prod_list:
                        rule = Rule()
                        rule.rule_set_name = self.name
                        rule.inc_keywords = [item[0], item[1]]
                        rule.exc_keywords = []
                        list_rules.append(rule)
            else:   #no and_keywords
                if len(nws) > 0:
                    prod_list = list(itertools.product(bws, nws))
                    for item in prod_list:
                        rule = Rule()
                        rule.rule_set_name = self.name
                        rule.inc_keywords = [item[0]]
                        rule.exc_keywords = [item[1]]
                        list_rules.append(rule)
                else:   #ONLY BASED_WORDS
                    for item in bws:
                        rule = Rule()
                        rule.rule_set_name = self.name
                        rule.inc_keywords = [item]
                        rule.exc_keywords = []
                        list_rules.append(rule)
        return list_rules

#bws = ['a', 'b']
#aws = []
#nws = ['1']
#print ComplexRule(None, None, None)._make_rules(bws,aws,nws)
