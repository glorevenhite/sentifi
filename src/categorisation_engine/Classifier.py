from Constant import *
from SentifiWordsBank import SentifiWordsBank
from Ruler import Ruler

from Rule import ComplexRule
from ClassifierUtils import ClassifierUtils
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
                print len(categories)


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

                            message = {'type': 'keywords', 'rule_id': rule_id}
                            client = Client()
                            result = client.send(message)

                            rule_json = simplejson.loads(result)

                            complex_rules = ComplexRule(cat_id, rule_json[str(rule_id)]).rules

                            for applied_rule in complex_rules:
                                if description_field.is_complied(applied_rule):
                                    dict_result.update({name: True})
                    else:
                        print "NONE"
                print dict_result

        return list_profiles

    def classify_profile(self, str_field_content, dict_ruleset):
        dict_ruleset = ClassifierUtils().get_list_ruleset_given_phase("'Category 1'")
        str_field_content = "I am financial analyst"
        print dict_ruleset

        list_rules = dict_ruleset['Category 1']
        print list_rules

        print "There are %s rules in total"  %len(list_rules)

        for rule_item in list_rules.items():
            topic = rule_item[0]
            keywords = rule_item[1]

            #Building set of keywords from vocabulary in respective rule


        #print dict_ruleset


            for ruleset in list_rulesets:
                kws = SentifiWordsBank().build_keywords(ruleset)
                keywords.append(kws)


            tokenized_content = []
            for kw in keywords:
                tokenized_content.append(SentifiWordsBank().tokenizer(raw_field_content, kw))

            for tc in tokenized_content:
                #HASHED tokenized_content by spliting with space
                hashed_tokenized_content = tc.split()

            index = 0
            for kw in keywords:
                #Check whether CONTENT satisfy ruleset, i.e., containing keywords
                if (set(hashed_tokenized_content) & set(kw)):
                    #print set(hashed_tokenized_content) & set(kw)

                    #select appropriate CLASS to classify

                    return PROFILE[index]
                else:
                    index += 1


    def classify_sub_category(self):


        pass

    def is_complied(self, field, list_ruleset):
        pass

    def _build_list_rulesets_per_field(self, fields, step):
        pairs = []

        for field in fields:
            list_rulesets = Ruler().load_list_rulesets(field, step)
            pair = []
            pair.append(field)
            pair.append(list_rulesets)
            pairs.append(pair)

        return pairs

    def _get_field_contents(self, profile):
        result = []

        result.append(profile.fullname)
        result.append(profile.description)

        return result

    def _get_inclusion_keywords_given_rule_id(self, rule_id):
        inclusion = ClassifierUtils()._get_included_keywords_for_given_rule_id(rule_id)
        return inclusion

    def _get_exclusion_keywords_given_rule_id(self, rule_id):
        exclusion = ClassifierUtils()._get_excluded_keywords_for_given_rule_id(rule_id)
        return exclusion

    def _build_wordsbank_from_rule_id(self, rule_id):
        inclusion = self._get_inclusion_keywords_given_rule_id(rule_id)
        exclusion = self._get_exclusion_keywords_given_rule_id(rule_id)
        wordsbank = list (set(inclusion) | set(exclusion))
        return wordsbank

    def _get_list_rulesets_given_phase(self, phase, field):
        results = ClassifierUtils().get_list_ruleset_given_phase_and_field(phase, field)






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



