""" Alternative switch function in Python """

def individual():
    ruleset_count = 1 #SELECT
    rs1 = ['believer', 'consultant', 'i' , 'my', 'owner', 'student']

    rulesets = []
    rulesets.append(rs1)

    return rulesets

def organisation():
    ruleset_count = 2 #SELECT
    rs1 = ['we', 'our', 'provider']
    rs2 = ['.com', 'bank', 'market', 'ltd.', 'limited', 'bv', 'llc']

    rulesets = []
    rulesets.append(rs1)
    rulesets.append(rs2)

    return rulesets

def news():
    rulesets = []
    return rulesets


Switcher = {
            0:individual,
            1:organisation,
            2:news
           }
