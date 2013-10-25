from Constant import *
from Rule import ComplexRule
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

            #for each phase,
            for phase in PHASE_VALUES:

                #build message to send server to get CATEGORIES in this phase
                message = {'type': 'categories_name', 'phase': phase}
                client = Client()
                result = client.send(message)
                categories = simplejson.loads(result)[phase]

                #Traverse universe of CATEGORIES
                for name in categories:
                    d = dict(name)
                    cat_id = d.keys()[0]

                    #Message to get RULES
                    message = {'type': 'rules', 'category_id': cat_id, 'field_id': FIELD_TWITTER_DESCRIPTION}
                    client = Client()
                    result = client.send(message)
                    rules = simplejson.loads(result)

                    dd = dict(rules)
                    if len(rules[cat_id]) > 0:
                        #Traverse in university of RULES
                        for rule_id in dd[cat_id]:

                            client = Client()
                            result = client.send({'type': 'keywords', 'rule_id': rule_id})

                            rule_json = simplejson.loads(result)

                            complex_rules = ComplexRule(cat_id, rule_json[str(rule_id)]).rules

                            for applied_rule in complex_rules:
                                if description_field.is_complied(applied_rule):
                                    print result
                                    dict_result.update({name: True})

                    else:
                        print rules[cat_id]
                print dict_result

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



