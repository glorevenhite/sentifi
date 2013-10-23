from Constant import *
from TwitterProfile import TwitterProfile
from SentifiWordsBank import SentifiWordsBank
from Rule import Rule
from Ruler import Ruler
from ClassifierUtils import ClassifierUtils

class Classifier(object):

    """ Here we pass a list of TwitterProfile(fullname, description)"""
    def classify_twitter_profile(self, list_profiles):
        output_profiles = []

        classifies = []
        dict_phases = Phases.VALUES      #{'PT':'PROFILE TYPE', 'PG':'PROFILE GROUP', 'C1':'CATEGORY 1', 'C2':'CATEGORY2'}
        dict_fields = Fields.VALUES            #Fullname - Description

        #Traverse each profile in set of profiles
        for profile in list_profiles:
            field_contents = self._get_field_contents(profile)

            #Identify PROFILE_TYPE
            #pairs = self._build_list_rulesets_per_field(field_contents, 'PT')    #Load rulesets

            #classifies.append(self.classify_profile_type(pairs, 'PT'))
            #profile.profile_type = self.classify_profile_type(pairs)

            #Identify CATEGORY_2
            #pairs = self._build_list_rulesets_per_field(FIELDS, 'C2')
            #profile.category2 = self.classify_profile_type(pairs, category)

            #Identify CATEGORY_1
            pairs = self._build_list_rulesets_per_field(FIELDS, 'C1')
            profile.category1 = self.classify_profile_type(pairs)

            #Identify GROUP_PUBLISHER
            #pairs = self._build_list_rulesets_per_field(FIELDS, 'PG')
            #profile.profile = self.classify_profile_type(pairs)

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
print Classifier()._build_wordsbank_from_rule_id(119)