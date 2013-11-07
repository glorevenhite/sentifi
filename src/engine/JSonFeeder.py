__author__ = 'vinh.vo@sentifi.com'
from SentifiCategory import SentifiCategory
from SentifiField import SentifiField
from SentifiQuery import SentifiQuery
from Constant import *

import urllib2
import simplejson
import pprint


class JSonFeeder(object):

    def get_list_categories(self):
        cat = SentifiCategory()
        cat.name = self.json_data['name']
        cat.parent = self.json_data['parent']
        cat.exclusion = self.json_data['exclusions']

        queries = dict(self.json_data['keywords'])
        for q in queries:
            query = SentifiQuery()
            query.field = q['keywords']['field']
            query.based_words = q['rules']['words']
            query.and1_words = q['keywords']['rules']['and1']
            query.and2_words = q['keywords']['rules']['and2']
            query.not_words = q['keywords']['rules']['not']
            cat.queries.append(q)

        return cat

    def get_list_keywords_by_category_id(self, cat_id):
        url = END_POINT_URL + 'getCategoryKeywordById?id={0}'.format(cat_id) + END_POINT_KEY
        req = urllib2.Request(url, None)
        opener = urllib2.build_opener()
        f = opener.open(req)

        return simplejson.loads(f.read())


    def get_list_categories(self):
        url = END_POINT_URL + 'getCategoryList?' + END_POINT_KEY
        req = urllib2.Request(url, None)
        opener = urllib2.build_opener()
        f = opener.open(req)

        return simplejson.loads(f.read())

    def get_list_categories_by_parent_id(self, parent_id):
        json_data = self.get_list_categories()

        list_result = []
        for item in json_data:
            if parent_id is None:
                if item['parent_id'] is parent_id:
                    list_result.append(dict(item))
            else:
                if item['parent_id'] == str(parent_id):
                    list_result.append(dict(item))

        return list_result

    def get_category_name_by_id(self, cat_id):
        json_data = self.get_list_categories()

        for item in json_data:
            if item['id'] == str(cat_id):
                return item['name']

    def get_category_id_by_name(self, cat_name):
        json_data = self.get_list_categories()

        for item in json_data:
            if item['name'] == str(cat_name):
                return item['id']

    def get_sentifi_categories(self, parent_name, field_name):
        pass

    def get_sentifi_categories(self, parent_name, field_name):
        json_data = self.get_list_categories()

        parent_id = self.get_category_id_by_name(parent_name)

        #get list of ids of categories
        list_ids = []
        for item in json_data:
            if parent_name is not None:
                if item['parent_id'] == str(parent_id):
                    list_ids.append(item['id'])
            else:
                if item['parent_id'] is None:
                    list_ids.append(item['id'])

        list_results = []
        # Having list of ids of all categories belong to a specific category, looking for all childs
        for id in list_ids:
            #looking for rules for this category
            json_data_rules = self.get_list_keywords_by_category_id(id)

            #Do not have any rules
            if json_data_rules is not None:
                # Having rules
                cat = SentifiCategory()
                cat.id = id
                cat.name = self.get_category_name_by_id(id)     # OPTIMIZE HERE
                cat.parent = parent_name
                keys = dict(json_data_rules).keys()

                #Having exclusion
                if 'exclusions' in keys:
                    if len(json_data_rules['exclusions']):
                        cat.exclusion.extend([item.strip().lower() for item in json_data_rules['exclusions'].split(",")])
                else:
                    cat.exclusion = []

                #Having keywords
                if 'keywords' in keys:
                    fields = json_data_rules['keywords']

                    for f in fields:
                        #Taking only rules for given field_name
                        if f['field'] == str(field_name):
                            queries = f['rules']
                            for q in queries:
                                query = SentifiQuery()
                                query.field = f['field']
                                #query.based_words = q['keyword'].split(",")
                                if len(q['keyword']):
                                    query.based_words.extend([item.strip().lower() for item in q['keyword'].split(",")])
                                if len(q['and'][0]):
                                    query.and1_words.extend([item.strip().lower() for item in q['and'][0].split(",")])
                                if len(q['and'][1]):
                                    query.and2_words.extend([item.strip().lower() for item in q['and'][1].split(",")])
                                if len(q['not']):
                                    query.not_words.extend([item.strip().lower() for item in q['not'].split(",")])
                                cat.queries.append(query)

                            list_results.append(cat)

        return list_results

    def get_parent_name(self, cat_name):
        json_data = self.get_list_categories()

        for item in json_data:
            if item['name'] == str(cat_name):
                parent_id = item['parent_id']

        parent_name = self.get_category_name_by_id(parent_id)

        return parent_name



if __name__ == "__main__":

    #pprint.pprint(JSonFeeder().get_list_keywords_by_category_id(45))
    #pprint.pprint(JSonFeeder().get_list_categories())
    #pprint.pprint(JSonFeeder().get_list_categories_by_parent_id(None))
    #pprint.pprint(JSonFeeder().get_list_categories_by_parent_id(2))
    #pprint.pprint((JSonFeeder().get_category_name_by_id(1)))
    #pprint.pprint((JSonFeeder().get_sentifi_categories('Financial Market Professionals', TWITTER_DESCRIPTION)))
    string = "abc, def"
    list_a = []
    list_a.extend([item.strip() for item in string.split(",")])
    print len(list_a)
    pass