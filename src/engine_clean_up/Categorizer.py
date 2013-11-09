
from MySQLUtils import MySQLUtils
from SentifiCategory import SentifiCategory
from SentifiField import SentifiField
from SentifiQuery import SentifiQuery
from SentifiTwitterProfile import SentifiTwitterProfile
from JSonFeeder import JSonFeeder
from Utils import *
from Constant import *
import shelve

import pprint


class Categorizer(object):
    def categorizer(self, profile, list_sentifi_categories, json_category_names):

        #Take the fields need to be scan
        fields = profile.get_fields()
        field_description = fields[2]

        #List of cat_id
        parent = CAT1_PARENT
        list_candidates = []

        #For each pid, looking for the name then making the candidate category to which profile is assigned
        for pid in parent:
            sentifi_category = JSonFeeder.get_sentifi_category_by_field(pid, TWITTER_DESCRIPTION, list_sentifi_categories)
            list_candidates.extend(sentifi_category)


        print len(list_candidates)

        #Taking array of results by examine the field to the list of candidates
        list_weighting = self.check_field_against_categories(field_description, list_candidates)
        list_candidate_names = [cat.name for cat in list_candidates]

        print list_candidate_names
        print list_weighting

        profile.category1 = get_candidate_name(list_weighting, list_candidate_names)

        profile.profile_group = JSonFeeder().get_parent_name(profile.category1, json_category_names)
        profile.profile_type = JSonFeeder().get_parent_name(profile.profile_group, json_category_names)
        print list_candidate_names
        print(list_weighting)

        #############################################################
        #parent = CAT2_PARENT_ID
        parent2 = profile.category1
        pid = JSonFeeder().get_category_id_by_name(parent2, json_category_names)
        list_candidates_2 = []
        list_candidates_2.extend(JSonFeeder().get_sentifi_category_by_field(pid, TWITTER_DESCRIPTION, list_sentifi_categories))

        if len(list_candidates_2):
            list_weighting_2 = self.check_field_against_categories(field_description, list_candidates_2)
            list_candidate_names_2 = [cat.name for cat in list_candidates_2]

            profile.category2 = get_candidate_name(list_weighting_2, list_candidate_names_2)

        else:
            profile.category2 = None


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
        content = unicode(sentifi_field.content).encode('utf-8')
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
        print "---------", content, '<<>>', sentifi_category.name
        print list_rules
        for rules in list_rules:
            if isinstance(rules, tuple):  # tuple
                if match_and(rules, content):
                    score += len(rules)
            elif type(rules) == type(u''):
                list_keywords = [rules]
                if match_and(list_keywords, content):
                    print list_keywords, 'against content of:', content
                    score += len(rules.split())
            else:
                print rules, type(rules)
        return score

if __name__ == "__main__":
    #print len(list_sentifi_categories)
    #print len(json_category_names)
    #
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
    #
    #profile = SentifiTwitterProfile([1, 'Truong Vinh', 'glorevenhite', 'Computational Finance, Productivity and Standardization'])
    #Categorizer().categorizer(profile, list_sentifi_categories, json_category_names)
    #profile.display()
    try:
        database = shelve.open(PATH_CACHE)
        list_sentifi_categories = database['sc']
        json_category_names = database['cn']
        database.close()

        connection = MySQLUtils().connection
        cursor = connection.cursor()
        sql = "SELECT * FROM {0} " .format(TABLE_PROFILES_INPUT)
        cursor.execute(sql)
        rows = cursor.fetchall()

        f = open('log.txt', 'w')

        for row in rows:
            p = SentifiTwitterProfile(row)
            Categorizer().categorizer(p, list_sentifi_categories, json_category_names)
            arr_values = p.to_array()

            string = ['%s']*len(arr_values)

            #Joining list of %s by comma
            var_st = ','.join(string)

            #Building query string
            query_str = 'INSERT INTO ' + TABLE_PROFILES_OUTPUT + ' VALUES(%s)' % var_st

            #Execute query and commit
            cursor.execute(query_str, arr_values)

            connection.commit()
    except Exception, e:
        f.write(str(e) + '\n')





