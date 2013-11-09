from SentifiCategory import SentifiCategory
from SentifiQuery import SentifiQuery

__author__ = 'vinh.vo@sentifi.com'
from Constant import *

import urllib2
import simplejson
import pprint
import shelve


class JSonFeeder(object):

    @staticmethod
    def get_json_categories():
        url = END_POINT_URL + 'getCategoryList?' + END_POINT_KEY
        req = urllib2.Request(url, None)
        opener = urllib2.build_opener()
        f = opener.open(req)
        return simplejson.loads(f.read())

    def get_list_categories(self):
        json_data = self.get_json_categories()

        list_cat = []
        for item in json_data:
            sc = SentifiCategory()
            sc.id = item['id']
            sc.name = item['name']
            sc.parent = item['parent_id']
            list_cat.append(sc)

        return list_cat

    @staticmethod
    def get_category_name_by_id(category_id, json_category_name):
        for item in json_category_name:
            if item.id == str(category_id):
                return item.name

    def parser(self):
        list_results = []

        json_categories = self.get_json_categories()

        for item in json_categories:
            json_rules = self.get_list_keywords_by_category_id(item['id'])

            if json_rules is not None:
                pprint.pprint(json_rules)

                sc = SentifiCategory()
                keys = dict(item).keys()
                if 'parent_id' not in keys:
                    break
                sc.id = item['id']
                sc.name = item['name']

                sc.parent = item['parent_id']
                keys = dict(json_rules).keys()

                #Having exclusion
                if 'exclusions' in keys:
                    if len(json_rules['exclusions']):
                        sc.exclusion.extend([item.strip().lower() for item in json_rules['exclusions'].split(",")])
                else:
                    sc.exclusion = []

                #Having keywords
                if 'keywords' in keys:
                    fields = json_rules['keywords']

                    # Foreach channel: Twitter name, twitter_description, linked name
                    for f in fields:
                        #if f['field'] == TWITTER_DESCRIPTION    # ONLY CONSIER TWITTER DESCRIPTION HERE, CHANGE LATER
                        keys = dict(f).keys()

                        if 'rules' in keys:
                            queries = f['rules']
                            for q in queries:
                                query = SentifiQuery()
                                query.field = f['field']
                                #query.fulltime = f['fulltime']     # split()
                                #query.partime = f['partime']   #split()
                                if len(q['keyword']):
                                    query.based_words.extend([item.strip().lower() for item in q['keyword'].split(",")])
                                if len(q['and'][0]):
                                    query.and1_words.extend([item.strip().lower() for item in q['and'][0].split(",")])
                                if len(q['and'][1]):
                                    query.and2_words.extend([item.strip().lower() for item in q['and'][1].split(",")])
                                if len(q['not']):
                                    query.not_words.extend([item.strip().lower() for item in q['not'].split(",")])
                                    #print query.get_list_simple_rules()

                                sc.queries.append(query)
                    list_results.append(sc)
        return list_results

    @staticmethod
    def get_sentifi_category_by_field(parent_id, field, list_sentifi_categories):
        list_result = []
        try:
            if parent_id is None:
                for sc in list_sentifi_categories:
                    if sc.parent == parent_id:
                        qs = []
                        for q in sc.queries:
                            if q.field == field:
                                qs.append(q)
                        sc.queries = qs
                        list_result.append(sc)
            else:
                for sc in list_sentifi_categories:
                    if sc.parent == str(parent_id):
                        qs = []
                        for q in sc.queries:
                            if q.field == field:
                                qs.append(q)
                        sc.queries = qs
                        list_result.append(sc)
        except Exception, e:
            print e
        return list_result


    def get_list_keywords_by_category_id(self, cat_id):
        url = END_POINT_URL + 'getCategoryKeywordById?id={0}'.format(cat_id) + END_POINT_KEY
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

    def get_category_name_by_id2(self, cat_id, json_data):

        for item in json_data:
            if item['id'] == str(cat_id):
                return item['name']

    @staticmethod
    def get_category_id_by_name(cat_name, list_data):
        for item in list_data:
            if item.name == str(cat_name):
                return item.id

    def get_sentifi_categories(self, parent_name, field_name, json_data_list_categories):
        #parent_id = self.get_category_id_by_name(parent_name)
        parent_id = self.get_category_id_by_name(parent_name, json_data_list_categories)

        #get list of ids of categories
        list_ids = []
        for item in json_data_list_categories:
            if parent_name is not None:
                if item['parent_id'] == str(parent_id):
                    list_ids.append(item['id'])
            else:
                if item['parent_id'] is None:
                    list_ids.append(item['id'])

        #PARSE JSON TO OBJECT
        list_results = []
        # Having list of ids of all categories belong to a specific category, looking for all childs
        for id in list_ids:
            #looking for rules for this category
            json_data_rules = self.get_list_keywords_by_category_id(id)


            #Having rules
            if json_data_rules is not None:
                cat = SentifiCategory()
                cat.id = id
                cat.name = self.get_category_name_by_id(id, json_data_list_categories)     # OPTIMIZE HERE
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
                        #Taking only rules for given field_name (Description
                        if f['field'] == str(field_name):
                            queries = f['rules']
                            for q in queries:
                                query = SentifiQuery()
                                query.field = f['field']
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

    def get_parent_name(self, cat_name, json_data_list_categories):

        for item in json_data_list_categories:
            if item.name == str(cat_name):
                parent_id = item.parent
                parent_name = self.get_category_name_by_id(parent_id, json_data_list_categories)
                return parent_name


if __name__ == "__main__":

    #pprint.pprint(JSonFeeder().get_list_keywords_by_category_id(45))
    #pprint.pprint(JSonFeeder().get_list_categories())
    #pprint.pprint(JSonFeeder().get_list_categories_by_parent_id(None))
    #pprint.pprint(JSonFeeder().get_list_categories_by_parent_id(2))
    #pprint.pprint((JSonFeeder().get_category_name_by_id(1)))
    #pprint.pprint((JSonFeeder().get_sentifi_categories('Financial Market Professionals', TWITTER_DESCRIPTION)))
    #string = "abc, def"
    #list_a = []
    #list_a.extend([item.strip() for item in string.split(",")])
    #print len(list_a)
    #print JSonFeeder().get_parent_name('Financial Analyst', json_category_names)

    #database = shelve.open(PATH_CACHE)
    #list_sentifi_categories = database['sc']
    #json_category_names = database['cn']
    #database.close()
    #
    #for sc in list_sentifi_categories:
    #    if sc.name == "P":
    #        print sc.parent
    #        break
    # JSonFeeder().parser()
    pass
