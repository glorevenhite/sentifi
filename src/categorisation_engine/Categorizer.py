__author__ = 'vinh.vo@sentifi.com'

from SentifiField import SentifiField
from Constant import *
from Client import Client
from TwitterProfile import TwitterProfile
from MySQLUtils import MySQLUtils

import numpy


class Categorizer(object):

    def categorize_twitter_profile_step(self, profile):
        print "Profile:", profile.display()

        #taking examining fields
        field_full_name = SentifiField(FIELD_TWITTER_FULL_NAME_ID, profile.fullname)
        field_screen_name = SentifiField(FIELD_TWITTER_SCREEN_NAME_ID, profile.screen_name)
        field_description = SentifiField(FIELD_TWITTER_DESCRIPTION_ID, profile.description)

        # Put above fields into a list
        fields = {TWITTER_FULL_NAME: field_full_name, TWITTER_SCREEN_NAME: field_screen_name, TWITTER_DESCRIPTION: field_description}
        print "1st STAGE: Identifying Profile Type..."
        stage = 'Profile Type'
        parent = "NULL"
        profile.profile_type = self._assign_class(stage, parent, fields)

        ##################################################################
        print "2nd STAGE: Identifying Publisher Group..."
        stage = 'Publisher Group'
        parent = profile.profile_type
        profile.profile_group = self._assign_class(stage, parent, fields)

        # Whether Person or Organisation
        print "3rd STAGE: Identifying Category 1..."
        stage = 'Category 1'
        parent = profile.profile_group
        profile.category1 = self._assign_class(stage, parent, fields)

        ######################################################################################
        print "4th STAGE: Identifying Category 2..."
        stage = 'Category 2'
        parent = profile.category1
        profile.category2 = self._assign_class(stage, parent, fields)

        profile.display()

        return profile

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

if __name__ == "__main__":
    connection = MySQLUtils().connection

    cursor = connection.cursor()

    sql = "SELECT * FROM {0} " .format(TABLE_PROFILES)
    cursor.execute(sql)

    rows = cursor.fetchall()

    list_profile = []
    for row in rows:
        p = TwitterProfile(row)
        p = Categorizer().categorize_twitter_profile_step(p)
        p.display()
        arr_values = p.to_array()

        string = ['%s']*len(arr_values)

        #Joining list of %s by comma
        var_st = ','.join(string)

        #Building query string
        query_str = 'INSERT INTO ' + 'results' + ' VALUES(%s);' % var_st

        #Execute query and commit
        cursor.execute(query_str, arr_values)
        connection.commit()



    #list_profile = Categorizer().categorize_twitter_profile_step(list_profile)

    #p = TwitterProfile([239, 'dividata', 'dividata .com', 'Dividend Stock Analysis and Dividend History'])
    #list_profiles = [p]
    #Categorizer().categorize_twitter_profile_step(list_profiles)

    #p = TwitterProfile([239, 'Luke_McLachlan', 'Luke McLachlan', 'Full-time day trader: Trading major FX pairs, UK & US large-caps, and Gold / Silver / Oil !'])
    #Categorizer().categorize_twitter_profile_step(p)

    #p = TwitterProfile([239, 'stockhunter1984', ' StockInterceptor.com', 'We are technical traders and we want to profit in the stock market! We use our Mobile Application to connect traders around the world!'])
    #list_profiles = [p]
    #Categorizer().categorize_twitter_profile_step(list_profiles)

    #p = TwitterProfile([4557, 'felix_schwarz', 'Felix Schwarz', 'OS X and iOS developer, author of Remote Buddy, Spacious, HIDRemote and Candelair, CEO of IOSPIRIT'])
    #Categorizer().categorize_twitter_profile_step(p)

    #p = TwitterProfile([123, 'john_smith', 'john smith', 'i am financial journalist'])
    #Categorizer().categorize_twitter_profile_step(p)

