__author__ = 'vinh.vo@sentifi.com'

import re
import operator
import numpy
import shelve
from Constant import *


def match_and(list_keywords, content):
    re_inclusion = []
    global list_keyword_regex

    for keyword in list_keywords:
        re_inclusion.append(list_keyword_regex[keyword])

    if re_inclusion:
        return all(r.search(content) for r in re_inclusion)
    else:
        return False


def match_or(keywords, content):
    re_inclusion = []
    score = 0
    global list_keyword_regex
    for kw in keywords:
        re_inclusion.append(list_keyword_regex[kw])

    if re_inclusion:
        for r in re_inclusion:
            if r.search(content):
                score += 1
    return score


def split_into_chunks(list_item, n):
        for i in xrange(0, len(list_item), n):
            yield list_item[i:i+n]


def match_not(keywords, content):
    re_inclusion = []
    global list_keyword_regex

    for keyword in list(keywords):
        re_inclusion.append(list_keyword_regex[keyword])

    if re_inclusion:
        for r in re_inclusion:
            if r.search(content):
                return True

    return False
    #return any(r.search(content) for r in re_inclusion)


def get_max_score(list_results, list_category_names):

    a = numpy.sum(list_results, axis=0)
    return list_category_names[numpy.argmax(a)]


def get_candidate_name(list_results, list_category_names):
    if len(list_results):
        if max(list_results) > 0:
            return list_category_names[numpy.argmax(list_results)]
    return None


def get_max_element_by_value(dict_values):
    return max(dict_values.iteritems(), key=operator.itemgetter(1))[0]


if __name__ == "__main__":
    pass
    list_keywords_test = ['investor']
    content_test = "where investors intersect with opportunity."
    #print match_and(list_keywords_test, content_test)     # 0

    list_keywords_test = ['investors', 'opportunity']
    content_test = "where investors intersect with opportunity."
    #print match_or(list_keywords_test, content_test)     # 1
    #
    #results = [4, 4]
    #list_category_names = ['Person', 'Organisation']
    #print get_max_score_1(results, list_category_names)

    #print sorted(dict_results)

    #print sorted(dict_results[0].items(), key=lambda k: dict_results[0].items(), reverse=True)

    #print dict_results[0].items()
    #print "idafj", [k for k in dict_results[0].values()]

    #content = "i am a financial analyst"
    #keywords = ('financial', 'anf')
    #print match_and(keywords, content)
    #
    #text = "abc"
    #print len(list[text])
    #print type((1, ))


def get_keywords(list_categories):
    keywords = []
    for cat in list_categories:
        keywords.extend(cat.exclusion)
        for query in cat.queries:
            keywords.extend(query.based_words)
            keywords.extend(query.and1_words)
            keywords.extend(query.and2_words)
            keywords.extend(query.not_words)

    return list(set(keywords))


def make_keywords_lookup(keywords):
    list_keywords_regex = dict()

    for kw in keywords:
        list_keywords_regex[kw] = re.compile('\\b' + kw + '\\b')

    return list_keywords_regex

#print list_keyword_regex['financial']
database = shelve.open(PATH_CACHE)
list_sentifi_categories = database['sc']
json_category_names = database['cn']
database.close()

list_keywords = get_keywords(list_sentifi_categories)
#print list_keywords
#print len(list_keywords)
list_keyword_regex = make_keywords_lookup(list_keywords)
#print len(list_keyword_regex)
#print list_keyword_regex['financial']

#for item in list_sentifi_categories:
#    print len(item.exclusion)
#    print len(item.get_exclusion())



