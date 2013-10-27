from Constant import *
from ComplexRule import ComplexRule
from SentifiField import SentifiField
from TwitterProfile import TwitterProfile
from Client import Client

import simplejson


class Classifier(object):

    """ Here we pass a list of TwitterProfile(fullname, description).
        For each profile we take out all fields need to be examine.
        For each phase (PT, PG, Cat1, Cat2) we get all class (i.e. category) to which we assign field.
        Getting all rule in that class then examine whether field satisfies any rule in such rule set.
        If so, assign respective class to considering profile.
    """
    def classify_twitter_profile(self, list_profiles):

        #Traverse each profile in set of profiles
        for profile in list_profiles:
            dict_result = {}

            description_field = SentifiField(profile.description)
            field_id = 1

            #for each phase,
            for phase in PHASE_VALUES:

                #build message to send server to get CATEGORIES in this phase
                message = {'type': 'ruleset', 'phase': phase, 'field_id': field_id}
                client = Client()
                result = client.send(message)
                try:
                    ruleset = simplejson.loads(result)[phase]
                except:
                    pass
                dict_r = dict(ruleset)
                print len(dict_r)
                for rule in dict_r:
                    print rule
                    cr = ComplexRule(rule, dict_r.get(rule).keys()[0], dict_r.get(rule))
                    rules = cr.rules
                    for r in rules:
                        description_field.is_complied(r)

                #print ruletset

        return list_profiles


#
#Classifier().classify_profile(None, None)
#print Classifier()._build_wordsbank_from_rule_id(119)

json = {'screen_name': 'glorevenhite', 'description': 'I am a financial analyst', 'name': 'Vo Truong Vinh'}
p1 = TwitterProfile(json)
p1.description = "I am financial analysis"
p1.screen_name = "glorevenhite"


profiles = [p1]
Classifier().classify_twitter_profile(profiles)

#Server calling



