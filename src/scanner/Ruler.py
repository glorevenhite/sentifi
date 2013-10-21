from Constant import *
from Switcher import *
from Rule import *

class Ruler(object):
    def __init__(self):
        self.category = [
                         Profile().PER,
                         Profile().ORG,
                         Profile().NEWS,
                         ]
    def load_all_ruleset(self, category):
        index = self.category.index(category)
        return Switcher[index]()

    # Each list_rulesets contain collection of rulesets. Each ruleset identify the Category (Class) of given field
    def load_list_rulesets(self, field, step):
        if (step == 'PT'):
            if (field == 'FN'):
                list_rulesets = []

                list_rulesets.append(None)

                ruleset1 = [None]*8
                ruleset1[0] = Rule(['.com'], [])
                ruleset1[1] = Rule(['bank'], [])
                ruleset1[2] = Rule(['market'], [])
                ruleset1[3] = Rule(['ltd'], [])
                ruleset1[4] = Rule(['limited'], [])
                ruleset1[5] = Rule(['bv'], [])
                ruleset1[6] = Rule(['llc'], [])
                ruleset1[7] = Rule(['news'], [])

                list_rulesets.append(ruleset1)
                return list_rulesets
            else:
                #load ruleset for description
                ruleset1 = [None]*7
                ruleset1[0] = Rule(['believer'], [])
                ruleset1[1] = Rule(['consultant'], [])
                ruleset1[2] = Rule(['i'], [])
                ruleset1[3] = Rule(['my'], [])
                ruleset1[4] = Rule(['owner'], [])
                ruleset1[5] = Rule(['student'], [])
                ruleset1[6] = Rule(['financial-analyst'], []) #extent example for test

                ruleset2 = [None]*3
                ruleset2[0] = Rule(['we'],[])
                ruleset2[1] = Rule(['our'],[])
                ruleset2[2] = Rule(['provider'],[])

                list_ruleset = []
                list_ruleset.append(ruleset1)
                list_ruleset.append(ruleset2)
                return list_ruleset
        elif (step == 'C2'):
            pass
        else:
            pass


#print Ruler().load_all_ruleset('ORGANISATION')