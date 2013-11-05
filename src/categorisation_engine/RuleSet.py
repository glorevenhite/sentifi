__author__ = 'vinh.vo@sentifi.com'

from Rule import Rule
import numpy


class RuleSet(object):
    def __init__(self, list_records):
        self.rules = numpy.array(list_records)


    def get_list_category_ids(self):
        return sorted(set(self.rules[:, 0]))

    def get_list_category(self, cat_id):
        return self.rules[self.rules[:, 0] == cat_id]

    def get_list_ruleset(self):
        list_results = []

        # Get list of ruleset_id
        list_ids = sorted(set(self.rules[:, 2]))
        for id in list_ids:
            rs = self.rules[self.rules[:, 2] == id]
            list_results.append(rs)

        return list_results[0]

    def get_list_simple_rules(self):
        list_results = []
        inclusion_rules = self.rules[self.rules[:, 5] == '0']
        list_ids = sorted(set(inclusion_rules[:, 3]))    # 3rd-column
        for id in list_ids:
            r = self.rules[self.rules[:, 3] == id]
            rule = Rule(r)
            #rule.display()
            list_results.append(rule)

        return list_results

    def get_exclusion_set(self):
        return set(self.rules[self.rules[:, 5] == '1', 4])     # 5th-column

    def get_exclusion_regex_str(self):
        exclusion_set = self.get_exclusion_set()
        list_item = []
        if len(exclusion_set):
            for item in exclusion_set:
                list_item.append("!" + item)

        return " ".join(list_item)

    def display(self):
        print self.cat_name, ":", self.exclusion, ":", [r for r in self.rules]

#exclusion = ['fuck', 'dung']
#print RuleSet(None).get_exclusion_regex_str(exclusion)
#a = [['1', 'P' ,'1', '608', 'we', '1', '0'],['1', 'P', '1', '610', 'provider', '0', '0']]
#
#ar = numpy.array(a)
#print set(ar[ar[:, 5] == '1', 4])