from Constant import *
from TwitterProfile import TwitterProfile
from SentifiWordsBank import SentifiWordsBank
from Rule import Rule
from Ruler import Ruler

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
        dict_ruleset = {'analyst':{0:'financial analyst',1:'equity analyst'}}

    def classify_profile_type(self, pairs):
        #retrieve list of profile for indexing
        PROFILE = Profile().PROFILES

        for item in pairs:
            #tokenizer the content by adding hyphen between compound-words
            raw_field_content = item[0]    #field_content, i.e., fullname, description
            list_rulesets = item[1]


            #Build set of keywords from vocabulary in respective ruleset
            keywords = []
            tokenized_content = []
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