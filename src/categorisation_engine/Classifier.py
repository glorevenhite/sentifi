from Constant import *
from ComplexRule import ComplexRule
from Rule import Rule
from SentifiField import SentifiField
from TwitterProfile import TwitterProfile
from Client import Client

import simplejson

class Classifier(object):

    """ Here we pass a list of TwitterProfile(screen_name, fullname, description).
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
            fullname_field = SentifiField(profile.fullname)
            fields = {1: description_field, 3: fullname_field}

            for field in fields:
                field_id = field
                field_content = fields.get(field_id)

                #for each phase,
                for phase in PHASE_VALUES:
                    dict_r = self._get_rule(phase, field_id)
                    for rule in dict_r:

                         for dct_r in dict_r.get(rule):
                            r = Rule()
                            r.rule_set_name = rule
                            r.inc_keywords = dict_r.get(rule).get(dct_r)['status']['and']
                            r.exc_keywords = dict_r.get(rule).get(dct_r)['status']['not']

                            if field_content.is_complied(r):

                                profile.set_category(phase, r.rule_set_name)

                                message = {'type': 'parent', 'category_name': r.rule_set_name}
                                client = Client()
                                result = client.send(message)

                                value = simplejson.loads(result)[r.rule_set_name]
                                profile.set_category('Profile Group',value)

                                msg2 = {'type': 'parent', 'category_name': value}
                                client = Client()
                                result2 = client.send(msg2)

                                value = simplejson.loads(result2)[value]
                                profile.set_category('Profile Type',value)

        return list_profiles

    def _get_rule(self, phase, field_id):
         #build message to send server to get CATEGORIES in this phase
        message = {'type': 'ruleset', 'phase': phase, 'field_id': field_id}
        client = Client()
        result = client.send(message)
        ruleset = {}
        try:
            ruleset = simplejson.loads(result)[phase]
        except:
            pass
        dict_r = dict(ruleset)

        return dict_r

#
#Classifier().classify_profile(None, None)
#print Classifier()._build_wordsbank_from_rule_id(119)

json = {'screen_name': 'glorevenhite', 'description': 'I am a financial analyst', 'name': 'Vo Truong Vinh'}
p1 = TwitterProfile(json)
p1.description = "I am a financial analyst trader me portfolio manager"
p1.screen_name = "glorevenhite"


profiles = [p1]
Classifier().classify_twitter_profile(profiles)
for p in profiles:
    p.display()
#Server calling



