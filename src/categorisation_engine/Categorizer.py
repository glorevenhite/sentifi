__author__ = 'vinh.vo@sentifi.com'

from SentifiField import SentifiField
from Constant import *
from Client import Client
from TwitterProfile import TwitterProfile

import numpy


class Categorizer(object):

    def categorize_twitter_profile_step(self, list_profiles):
        for profile in list_profiles:

            print "Profile:", profile.display()

            #taking examining fields
            field_full_name = SentifiField(FIELD_TWITTER_FULL_NAME_ID, profile.fullname)
            field_screen_name = SentifiField(FIELD_TWITTER_SCREEN_NAME_ID, profile.screen_name)
            field_description = SentifiField(FIELD_TWITTER_DESCRIPTION_ID, profile.description)

            # Put above fields into a list
            fields = {TWITTER_FULL_NAME: field_full_name, TWITTER_SCREEN_NAME: field_screen_name, TWITTER_DESCRIPTION: field_description}
            print "STAGE: Identifying Profile Type..."
            stage = 'Profile Type'
            parent = "NULL"
            profile.profile_type = self._assign_class(stage, parent, fields)



            ##################################################################
            print "STAGE: Identifying Publisher Group..."
            stage = 'Publisher Group'
            parent = profile.profile_type
            profile.profile_group = self._assign_class(stage, parent, fields)


            # Whether Person or Organisation
            print "STAGE: Identifying Category 1..."
            stage = 'Category 1'
            parent = 'Financial Market Professionals'
            profile.category1 = self._assign_class(stage, parent, fields)

            ######################################################################################
            print "STAGE: Identifying Category 2..."
            stage = 'Category 2'
            parent = profile.category1
            profile.category2 = self._assign_class(stage, parent, fields)

    def _assign_class(self, stage, parent, fields):
        for field in fields.values():
            field_id = field.id
            #print field.content
            list_rules = self._get_rule_subset_by_phase_field_parent(stage, field_id, parent)

            if len(list_rules):
                #numpy array
                arr_rules = numpy.array(list_rules)
                #print arr_rules

                #checking the satisfaction
                assigned_class = field.is_complied(arr_rules)
                return assigned_class


    @staticmethod
    def _get_rule_subset_by_phase_field_parent(stage_name, field_id, parent_id):
        result = []

        message = {'type': 'rules', 'stage_name': stage_name, 'field_id': field_id, 'class_name': parent_id}
        client = Client()

        returned_data = dict(client.send(message))
        if returned_data.get('status') == SERVER_STATUS_OK:
            result = returned_data.get('data').get(parent_id)

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

    list_profiles = [p]

    #print Categorizer().categorize_twitter_profile(list_profile)
    #Categorizer()._get_classes_by_phase_name('Category 1')
    Categorizer().categorize_twitter_profile_step(list_profiles)
    list_profiles[0].display()
