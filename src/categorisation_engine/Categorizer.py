__author__ = 'vinh.vo@sentifi.com'
from SentifiField import SentifiField
from Constant import *
from Client import Client
from TwitterProfile import TwitterProfile
from CategorisationMatrix import CategorisationMatrix

class Categorizer(object):
    def categorize_twitter_profile(self, list_profiles):

        for profile in list_profiles:
            #declare Matrix of Categorisation Result
            matrix = {}

            #taking examining fields
            field_full_name = SentifiField(FIELD_TWITTER_FULL_NAME, profile.fullname)
            field_screen_name = SentifiField(FIELD_TWITTER_SCREEN_NAME, profile.screen_name)
            field_description = SentifiField(FIELD_TWITTER_DESCRIPTION, profile.description)

            # Put above fields into a list
            fields = {TWITTER_FULL_NAME: field_full_name, TWITTER_SCREEN_NAME: field_screen_name, TWITTER_DESCRIPTION: field_description}
            FIELDS = {3, 2, 1}
            # For each phase of categorisation process, i.e. Profile Type, Publisher Group, Category 1, Category 2
            #
            for stage in PHASE_VALUES:
                #creating matrix of categorisation result
                matrix = self._create_categorisation_result_matrix(fields.keys(), stage)

                # For each field, get all applicable rules.
                # Count how many time a field satisfies its own set of rules
                # Update values to matrix
                for field in FIELDS:
                    rule_set = self._get_rules_by_phase_and_field(stage, field)

                    print rule_set

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