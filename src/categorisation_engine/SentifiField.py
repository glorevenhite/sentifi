from Rule import Rule
from SentifiWordsBank import SentifiWordsBank
from RuleSet import RuleSet
from RuleUtils import *
import numpy

class SentifiField(object):
    def __init__(self, id, content):
        self.id = id
        self.content = content
        self.category = ""

    def is_complied(self, arr_rules):
        sorted_arr_rules = arr_rules[arr_rules[:, 6].argsort()]
        list_ids = list(set(sorted_arr_rules[:, 2]))
        #last_ruleset = sorted_arr_rules[len(sorted_arr_rules) - 1]

        for id in list_ids:
            arr_ruleset = arr_rules[arr_rules[:, 2] == id]
            rs = RuleSet(arr_ruleset)

            #Exclusion set            "
            #print "Exclusion set for ruleset:" , rs.get_exclusion_regex_str()
            #print "Determining..."
            #print "OK"
            exclusion_str_regex = rs.get_exclusion_regex_str()
            if len(exclusion_str_regex) > 0 and match(exclusion_str_regex, self.content):
                return arr_ruleset[0][1]    # Return class name

            #print "---------INCLUSION----------"
            # Processing inclusion set in each simple rule
            list_simple_rules = rs.get_list_simple_rules()
            for simple_rule in list_simple_rules:
                str_regex = simple_rule.get_regex_inclusion_str()
                #print "content:", self.content
                #print "regex:", str_regex
                if match(str_regex, self.content):
                    return simple_rule.class_name
        return None

    def _apply_rule(self, tokenized_content, inclusion, exclusion):

        #Check whether content contains any word in exclusion set
        exc = set(tokenized_content) & set(exclusion)
        if len(exc) > 0:    # contains word in exclusion set
            return False

        innersection = set(tokenized_content) & set(inclusion)

        #Check whether the inclusion set is completely contained in content
        if len(innersection) == len(set(inclusion)):
            return True
        else:
            return False


    def apply_rule_subset(self, subset):
        score = 0

        #check with the exclusion
        exclusion = subset.exclusion
        for keyword in exclusion:
            if self.content.find(keyword) > 0:
                return score
        #print exclusion

        #check each rule
        list_rules = subset.rules
        #print list_rules

        for rules in list_rules:
            flag = True
            for keyword in rules:
                if self.content.find(keyword) < 0:
                    flag = False
            if flag is True:
                score += 1
        return score



#
#content = " I am an financial analyst"
#rule = Rule()
#rule.rule_set_name = "financial analyst"
#rule.inc_keywords = ['financial analyst']
#field = SentifiField(content)
#print field.is_complied(rule)
#