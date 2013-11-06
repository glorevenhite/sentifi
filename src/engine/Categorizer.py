__author__ = 'vinh.vo@sentifi.com'

from SentifiCategory import SentifiCategory
from SentifiField import SentifiField
from SentifiQuery import SentifiQuery
from ResultMatrix import ResultMatrix
from Utils import *


class Categorizer(object):
    def categorizer(self, profile):
        fields = profile.get_fields()

        stage = "Profile Type"
        parent = "NULL"
        list_field_names = self.get_list_field_names()
        list_category_names = self.get_list_category_names()
        result_matrix = ResultMatrix(list_field_names, list_category_names)

        for f in fields:
            field_name = f.name
            list_categories = self.get_categories(stage, parent, field_name)
            pass



        #stage = "Publisher Group"
        #parent =



        #taking all the fields
            pass

    def check(self, sentifi_field, sentifi_category):
        score = 0
        #Extract only content
        content = sentifi_field.content
        print "content:", content

        #Extract exclusion
        exclusion = sentifi_category.get_exclusion()
        print "exclusion:", exclusion

        if exclusion:
            if self.is_contained(exclusion, content):
                return score

        #Extract rules
        list_rules = sentifi_category.get_rules()
        for rules in list_rules:
            if self.is_contained(rules, content):
                score += 1
        print list_rules

        return score

    def check_inclusion(self, text, list_keywords):
        pass

    def check_exclusion(self, text, list_keywords):

        pass

    def is_contained(self, list_keywords, text):
        return look(list_keywords, text)



#text = " I am a financial journalist"
#list_keywords = ['financial', 'business']
#print Categorizer().is_contained(list_keywords, text)

if __name__ == "__main__":
    field = SentifiField()
    field.content = " I am a Financial Product Analyst journalist"
    field.channel = "TWITTER"

    q1 = SentifiQuery()
    q1.based_words = ['Financial']
    q1.and1_words = ['Product', 'Services']
    q1.and2_words = ['Analyst']

    q2 = SentifiQuery()
    q2.based_words = ['Economist', 'Financial']
    q2.and1_words = ['Buy Side']

    category = SentifiCategory()
    category.name = "Financial Analyst"
    category.exclusion = ['Fraud Analyst', 'Junior Business Analyst']
    category.queries = [q1, q2]

    print Categorizer().check(field, category)






