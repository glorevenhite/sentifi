__author__ = 'vinh.vo@sentifi.com'
from SentifiField import SentifiField
from Constant import *
from Client import Client
from TwitterProfile import TwitterProfile
from CategorisationMatrix import CategorisationMatrix
from RuleSet import RuleSet
from Rule import Rule

class Categorizer(object):
    def categorize_twitter_profile(self, list_profiles):

        for profile in list_profiles:
            #declare Matrix of Categorisation Result
            matrix = {}

            #taking examining fields
            field_full_name = SentifiField(FIELD_TWITTER_FULL_NAME_ID, profile.fullname)
            field_screen_name = SentifiField(FIELD_TWITTER_SCREEN_NAME_ID, profile.screen_name)
            field_description = SentifiField(FIELD_TWITTER_DESCRIPTION_ID, profile.description)

            # Put above fields into a list
            fields = {TWITTER_FULL_NAME: field_full_name, TWITTER_SCREEN_NAME: field_screen_name, TWITTER_DESCRIPTION: field_description}

            # For each phase of categorisation process, i.e. Profile Type, Publisher Group, Category 1, Category 2
            #
            for stage in PHASE_VALUES:
                #creating matrix of categorisation result
                matrix = self._create_categorisation_result_matrix(fields.keys(), stage)

                # For each field, get all applicable rules.
                # Count how many time a field satisfies its own set of rules
                # Update values to matrix
                for field in fields.values():
                    field_id = field.id
                    list_rule_subset = self._get_rule_subset_by_phase_and_field(stage, field_id)

                    for subset in list_rule_subset:
                        score = field._apply_rule_subset(subset)
                        matrix.increase_by(field_id,)

                    print list_rule_subset
    def _get_rule_subset_by_phase_and_field(self, stage_name, field_id):
        message = {'type': 'rule_subset', 'phase': stage_name, 'field_id': field_id}
        client = Client()

        # format:
        # {cat_name:
        #   {subset_id:{'exclusion':[n1,n2,n3], 'rules':{rid:[a1,b1],rid:[a2,b1]}},
        #    subset_id:{'exclusion':[m1,m2,m3], 'rules':{rid:[x1,y1], rid:[x1,y2}}}
        dict_rule_subsets = dict(client.send(message))
        cat_name = dict_rule_subsets.keys()[0]

        for subset in dict_rule_subsets.get(cat_name):
            ss = RuleSet()
            ss.cat_name = cat_name
            ss.exclusion = subset.get('inclusion')
            rules = subset.get('rules')
            for rule in rules:
                r = Rule()
                r.inclusion = rule

    def _create_categorisation_result_matrix(self, field_names, phase):
        #get all classes to which a profile will be assigned in given phase

        list_class_names = self._get_classes_by_phase_name(phase)
        list_field_names = field_names
        matrix = CategorisationMatrix(list_field_names, list_class_names)

        return matrix
    def _get_rules_by_phase_and_field(self, stage_name, field_id):
        message = {'type': 'ruleset', 'phase': stage_name, 'field_id': field_id}
        client = Client()
        print message
        result = dict(client.send(message))

        return result

    def _get_classes_by_phase_name(self, phase):
        message = {'type': 'classes', 'phase': phase}
        client = Client()
        returned_data = dict(client.send(message))

        result = {}
        if returned_data['status'] == SERVER_STATUS_OK:
            result.update({phase: returned_data.get('data').get(phase)})

        return result.get(phase).values()

json = {'screen_name': 'glorevenhite', 'description': 'I am a financial analyst', 'name': 'Vo Truong Vinh'}
p = TwitterProfile(json)
p.screen_name = "glorevenhite"
p.description = "I am a financial analyst"
p.fullname = 'Vo Truong Vinh'

list_profile = [p]

Categorizer().categorize_twitter_profile(list_profile)