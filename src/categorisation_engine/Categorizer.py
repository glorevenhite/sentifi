__author__ = 'vinh.vo@sentifi.com'

from SentifiField import SentifiField
from Constant import *
from Client import Client
from TwitterProfile import TwitterProfile
from CategorisationMatrix import CategorisationMatrix
from RuleUtils import *
from RuleSet import RuleSet
from Rule import Rule

import numpy


class Categorizer(object):

    def categorize_twitter_profile_step(self, list_profiles):
        for profile in list_profile:
             #taking examining fields
            field_full_name = SentifiField(FIELD_TWITTER_FULL_NAME_ID, profile.fullname)
            field_screen_name = SentifiField(FIELD_TWITTER_SCREEN_NAME_ID, profile.screen_name)
            field_description = SentifiField(FIELD_TWITTER_DESCRIPTION_ID, profile.description)

            # Put above fields into a list
            fields = {TWITTER_FULL_NAME: field_full_name, TWITTER_SCREEN_NAME: field_screen_name, TWITTER_DESCRIPTION: field_description}

            # Whether Person or Organisation
            stage = 'Category 1'
            parent = "Financial Market Professionals"
            list_class_names = self._get_classes(stage, parent)

            ##Creating matrix
            #list_field_names = fields.keys()
            #list_class_names = self._get_classes(stage, parent)
            #matrix = CategorisationMatrix(list_field_names, list_class_names)
            #matrix.display()

            for field in fields.values():
                field_id = field.id
                print field.content
                list_rules = self._get_rule_subset_by_phase_field_parent(stage, field_id, parent)

                if len(list_rules):
                    #numpy array
                    arr_rules = numpy.array(list_rules)
                    #print arr_rules

                    #checking the satisfaction
                    assigned_class = field.is_complied(arr_rules)
                    print "Assigned class:", assigned_class

    @staticmethod
    def _get_parent_class_name(stage, cat_name):

        message = {'type': 'parent', 'category_name': cat_name}
        print "looking for parent for:", cat_name
        client = Client()
        result = dict(client.send(message))
        print result
        return result


    @staticmethod
    def _get_rule_subset_by_phase_field_parent(stage_name, field_id, parent_id):
        result = []

        message = {'type': 'rules', 'stage_name': stage_name, 'field_id': field_id, 'class_name': parent_id}
        client = Client()

        returned_data = dict(client.send(message))
        if returned_data.get('status') == SERVER_STATUS_OK:
            result = returned_data.get('data').get(parent_id)

        return result

    def _create_categorisation_result_matrix(self, field_names, phase):
        #get all classes to which a profile will be assigned in given phase

        list_class_names = self._get_classes_by_phase_name(phase)
        list_field_names = field_names

        matrix = CategorisationMatrix(list_field_names, list_class_names)

        return matrix

    def _create_categorisation_result_matrix2(self, field_names, phase, parent):
        #get all classes to which a profile will be assigned in given phase

        list_class_names = self._get_classes_by_phase_name(phase, parent)
        list_field_names = field_names

        matrix = CategorisationMatrix(list_field_names, list_class_names)

        return matrix

    @staticmethod
    def _get_rules_by_phase_and_field(stage_name, field_id):
        message = {'type': 'ruleset', 'phase': stage_name, 'field_id': field_id}
        client = Client()

        result = dict(client.send(message))

        return result


    @staticmethod
    def _get_classes(stage_name, parent_class):
        message = {'type': 'classes', 'stage': stage_name, 'parent_class': parent_class}
        client = Client()
        returned_data = dict(client.send(message))

        result = {}
        if returned_data['status'] == SERVER_STATUS_OK:
            result.update({stage_name: returned_data.get('data').get(stage_name)})
            return result.get(stage_name).values()
        return result

if __name__ == "__main__":

    json = {'screen_name': 'glorevenhite', 'description': 'I am a financial analyst', 'name': 'Vo Truong Vinh'}
    p = TwitterProfile(json)
    p.screen_name = "glorevenhite"
    p.description = "I am an equity analyst sell side"
    p.fullname = 'Vo Truong Vinh'

    list_profile = [p]

    #print Categorizer().categorize_twitter_profile(list_profile)
    #Categorizer()._get_classes_by_phase_name('Category 1')
    Categorizer().categorize_twitter_profile_step(list_profile)
