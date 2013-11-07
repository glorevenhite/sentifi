__author__ = 'vinh.vo@sentifi.com'
from MySQLUtils import MySQLUtils
#from SentifiCategory import SentifiCategory
#from SentifiField import SentifiField
#from SentifiQuery import SentifiQuery
from SentifiTwitterProfile import SentifiTwitterProfile
from JSonFeeder import JSonFeeder
from Utils import *
from Constant import *

import pprint


class Categorizer(object):
    def categorizer(self, profile):
        fields = profile.get_fields()

        field_description = fields[2]

        parent = CAT1_PARENT
        list_sentifi_categories = []
        for p in parent:
            parent_name = JSonFeeder().get_category_name_by_id(p)

            list_sentifi_categories.extend(JSonFeeder().get_sentifi_categories(parent_name, TWITTER_DESCRIPTION))

        list_result = self.check_field_against_categories(field_description, list_sentifi_categories)
        list_category_names = [cat.name for cat in list_sentifi_categories]

        profile.category1 = get_max_score_1(list_result, list_category_names)

        profile.profile_group = JSonFeeder().get_parent_name(profile.category1)

        profile.profile_type = JSonFeeder().get_parent_name(profile.profile_group)
        print list_category_names
        print(list_result)

        #############################################################
        #parent = CAT2_PARENT_ID
        parent2 = profile.category1

        list_sentifi_categories2 = []

        list_sentifi_categories2.extend(JSonFeeder().get_sentifi_categories(parent2, TWITTER_DESCRIPTION))
        if len(list_sentifi_categories2):
            list_result2 = self.check_field_against_categories(field_description, list_sentifi_categories2)

            list_category_names2 = [cat.name for cat in list_sentifi_categories2]

            profile.category2 = get_max_score_1(list_result2, list_category_names2)

            print list_category_names2
            print list_result2
        else:
            profile.category2 = None



        #sorted_results = sorted(list_results key=lambda k in )
        ##take the category have largest score in list result
        #assigned_category = sorted_list_results[0]
        #profile.profile_type = assigned_category

        #stage = "Publisher Group"
        #parent =

    # Checking whether fields satisfy
    def check_fields_against_categories(self, sentifi_fields, sentifi_categories):
        list_result = []

        # the input contains rules for all fields, so we need extract specific rules given field
        list_categories = self.get_categories(sentifi_categories)

        # For each field we will check it against a list of categories to know to which it can be classified
        # The result is an array of score indicates how good (how many time) a field contains keywords given
        for f in sentifi_fields:
            dict_results = self.check_field_against_categories(f, list_categories)
            list_result.append(dict_results)

        return list_result

    def check_field_against_categories(self, sentifi_field, sentifi_categories):
        list_results = []
        #list_category_names = [cat.name for cat in sentifi_categories]

        for cat in sentifi_categories:
            score = self.check(sentifi_field, cat)
            list_results.append(score)

        return list_results

    @staticmethod
    def get_categories(list_sentifi_categories, field):
        list_results = []

        for cat in list_sentifi_categories:
            queries = cat.queries
            for query in queries:
                if query.field == field:
                    list_results.append(cat)

        return list_results

    @staticmethod
    def check(sentifi_field, sentifi_category):
        score = 0
        #Extract only content
        content = sentifi_field.content
        #print "content:", content

        #Extract exclusion
        exclusion = sentifi_category.get_exclusion()
        #print "exclusion:", exclusion

        if len(exclusion):
            if match_not(exclusion, content):
                print "exclusion", exclusion
                score = 0
                return score

        #Extract rules
        list_rules = sentifi_category.get_rules()
        #print "inclusion:", list_rules
        print "---------"
        for rules in list_rules:
            #print rules
            if match_and(rules, content):
                print rules
                if type(rules) == type(list):
                    score += len(list(rules))
                else:
                    print type(rules)
                    score += 1
        print score
        return score

#text = " I am a financial journalist"
#list_keywords = ['financial', 'business']
#print Categorizer().is_contained(list_keywords, text)

if __name__ == "__main__":

    #field = SentifiField()
    #field.content = " I am a Financial Product Analyst Buy Side journalist"
    #field.channel = "TWITTER"
    #
    #q1 = SentifiQuery()
    #q1.based_words = ['Financial']
    #q1.and1_words = ['Product', 'Services']
    #q1.and2_words = ['Analyst']
    #
    #q2 = SentifiQuery()
    #q2.based_words = ['Economist', 'Financial']
    #q2.and1_words = ['Buy Side']
    #
    #category = SentifiCategory()
    #category.name = "Financial Analyst"
    #category.exclusion = ['Fraud Analyst', 'Junior Business Analyst']
    #category.queries = [q1, q2]
    #
    #q3 = SentifiQuery()
    #q3.based_words = ['Portfolio', 'Asset', 'Fund']
    #q3.and1_words = ['Manager']
    #
    #cat2 = SentifiCategory()
    #cat2.name = "Portfolio Manager"
    #cat2.exclusion = []
    #cat2.queries = [q3]
    #
    #list_categories = [category, cat2]
    #list_fields = [field]
    #
    #result = Categorizer().check_fields_against_categories(list_fields, list_categories)
    #print 'matrix:', result

    #profile = SentifiTwitterProfile([1, 'Truong Vinh', 'glorevenhite', 'I am a Financial Analyst'])
    #Categorizer().categorizer(profile)
    #profile.display()

    connection = MySQLUtils().connection

    cursor = connection.cursor()

    sql = "SELECT * FROM {0} " .format(TABLE_PROFILES)
    cursor.execute(sql)

    rows = cursor.fetchall()

    for row in rows:
        p = SentifiTwitterProfile(row)
        Categorizer().categorizer(p)
        p.display()
        arr_values = p.to_array()

        string = ['%s']*len(arr_values)

        #Joining list of %s by comma
        var_st = ','.join(string)

        #Building query string
        query_str = 'INSERT INTO ' + ' results ' + ' VALUES(%s)' % var_st

        #Execute query and commit
        cursor.execute(query_str, arr_values)

        connection.commit()






