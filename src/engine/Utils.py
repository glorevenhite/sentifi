__author__ = 'vinh.vo@sentifi.com'

import re
import operator
import numpy


def match_and(list_keywords, content):
    re_inclusion = []
    for keyword in list_keywords:
        re_inclusion.append(re.compile(keyword))

    return all(r.search(content) for r in re_inclusion)

def match_not(list_keywords, content):
    re_inclusion = []
    for keyword in list_keywords:
        re_inclusion.append(re.compile(keyword))

    return any(r.search(content) for r in re_inclusion)

def get_max_score(list_results, list_category_names):

    a = numpy.sum(list_results, axis=0)
    print numpy.argmax(a)
    return list_category_names[numpy.argmax(a)]

def get_max_score_1(list_results, list_category_names):

    return list_category_names[numpy.argmax(list_results)]


def get_max_element_by_value(dict_values):
    return max(dict_values.iteritems(), key=operator.itemgetter(1))[0]

def get_keywords_from_nth_box():
    pass


def get_inclusion():
    pass

if __name__ == "__main__":
    pass
    #list_keywords = ['financial', 'analyst']
    #content = "I am a financial analyst"
    #print match_and(list_keywords, content)
    #
    results = [4, 4]
    list_category_names = ['Person', 'Organisation']
    print get_max_score_1(results, list_category_names)

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


