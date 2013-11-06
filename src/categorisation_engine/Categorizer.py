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

        #print "1st STAGE: Identifying Profile Type..."
        stage = 'Profile Type'
        parent = "NULL"
        assigned_class = self._assign_class(stage, parent, fields)
        if assigned_class is not None:    # having identified profile_type
            profile.profile_type = assigned_class

            #moving to next step
            stage = 'Publisher Group'
            parent = profile.profile_type
            assigned_class = self._assign_class(stage, parent, fields)
            if assigned_class is not None:
                profile.profile_group = assigned_class

                # next step
                stage = 'Category 1'
                parent = profile.profile_group
                assigned_class = self._assign_class(stage, parent, fields)
                if assigned_class is not None:
                    profile.category1 = assigned_class

                    # next step
                    stage = 'Category 2'
                    parent = profile.category1
                    assigned_class = self._assign_class(stage, parent, fields)

                    if assigned_class is not None:
                        profile.category2 = assigned_class
                        return profile

        ##################################################################
        #print "2nd STAGE: Identifying Publisher Group..."
        #stage = 'Publisher Group'
        #parent = profile.profile_type
        #profile.profile_group = self._assign_class(stage, parent, fields)


        # Whether Person or Organisation
        assigned_class = ""
        if profile.profile_type == "P":
            publisher_groups = P_PUBLISHER_GROUP
        else:
            publisher_groups = O_PUBLISHER_GROUP

        for publisher_group in publisher_groups:
            #print "3rd STAGE: Identifying Category 1..."
            stage = 'Category 1'
            parent = publisher_group
            assigned_class = self._assign_class(stage, parent, fields)
            if assigned_class is not None:
                profile.category1 = assigned_class
                profile.profile_group = parent
                profile.profile_type = self._get_parent_class_name(parent)
                pass

        if profile.category1 is None:   # Cannot detect any category
            # if person => Non identified person

            # if organisation
            pass
        else:
            #profile.category1 = assigned_class
            ######################################################################################
            #print "4th STAGE: Identifying Category 2..."
            stage = 'Category 2'
            parent = profile.category1
            assigned_class = self._assign_class(stage, parent, fields)
            if assigned_class is not None:
                profile.category2 = assigned_class

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
    def _get_rules(stage_name, field_id):
        result = []

        message = {'type': 'rules', 'stage_name': stage_name, 'field_id': field_id}
        client = Client()

        returned_data = dict(client.send(message))
        if returned_data.get('status') == SERVER_STATUS_OK:
            result = returned_data.get('data')

        return result

    @staticmethod
    def _get_parent_class_name(class_name):
        result = []
        message = {'type': 'parent', 'category_name': class_name}
        client = Client()

        returned_data = dict(client.send(message))
        if returned_data.get('status') == SERVER_STATUS_OK:
            result = returned_data.get('data')
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

if __name__ == "__main__":
    #connection = MySQLUtils().connection
    #
    #cursor = connection.cursor()
    #
    #sql = "SELECT * FROM {0} " .format(TABLE_PROFILES)
    #cursor.execute(sql)
    #
    #rows = cursor.fetchall()
    #
    #for row in rows:
    #    p = TwitterProfile(row)
    #    p = Categorizer().categorize_twitter_profile_step(p)
    #    p.display()
    #    arr_values = p.to_array()
    #
    #    string = ['%s']*len(arr_values)
    #
    #    #Joining list of %s by comma
    #    var_st = ','.join(string)
    #
    #    #Building query string
    #    query_str = 'INSERT INTO ' + 'results' + ' VALUES(%s);' % var_st
    #
    #    #Execute query and commit
    #    cursor.execute(query_str, arr_values)
    #    connection.commit()
    #


    #list_profile = Categorizer().categorize_twitter_profile_step(list_profile)

    #p = TwitterProfile([239, 'dividata', 'dividata .com', 'Dividend Stock Analysis and Dividend History'])
    #list_profiles = [p]
    #Categorizer().categorize_twitter_profile_step(list_profiles)

    #p = TwitterProfile([239, 'Luke_McLachlan', 'Luke McLachlan', 'Full-time day trader: Trading major FX pairs, UK & US large-caps, and Gold / Silver / Oil !'])
    #Categorizer().categorize_twitter_profile_step(p)

    #p = TwitterProfile([239, 'stockhunter1984', ' StockInterceptor.com', 'We are technical traders and we want to profit in the stock market! We use our Mobile Application to connect traders around the world!'])
    #list_profiles = [p]
    #Categorizer().categorize_twitter_profile_step(list_profiles)
    #
    #p = TwitterProfile([4557, 'felix_schwarz', 'Felix Schwarz', 'OS X and iOS developer, author of Remote Buddy, Spacious, HIDRemote and Candelair, CEO of IOSPIRIT'])
    #Categorizer().categorize_twitter_profile_step(p)
    #
    #p1 = TwitterProfile([4568, 'johnshinal', 'johnshinal', 'Cover public & private tech cos., business & tech trends,\
    #                                                      and tech investing for http://t.co/VU9J5MO3le, http://t.co/jZ8zrF9ciP, http://t.co/sOOzJ3Xu2y, et al.'])
    #Categorizer().categorize_twitter_profile_step(p1)
    #
    #p2 = TwitterProfile([4683, 'GordonnanBroad', 'Gordon & Broad', 'Trading relentlessly and searching for unique alternative investments: non-traditional,  staying relevant -please check us out at - http://t.co/lowIBlbPc4'])
    #Categorizer().categorize_twitter_profile_step(p2)
    #
    #p = TwitterProfile([123, 'john_smith', 'john smith', 'i am financial journalist'])
    #Categorizer().categorize_twitter_profile_step(p)

    #Categorizer()._get_parent_class_name('Financial Analyst')

    #p = TwitterProfile([287, 'GovBrain', 'GovBrain', "Get Stock Trading Edge From Our Political Intelligence.We Know Government So You Don't Have To."])
    #Categorizer().categorize_twitter_profile_step(p)

    p = TwitterProfile([1254, 'abheekb', 'Abheek Bhattacharya', 'Wall Street Journal. Columnist, Heard on the Street.'])
    Categorizer().categorize_twitter_profile_step(p)
