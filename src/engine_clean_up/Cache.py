from JSonFeeder import JSonFeeder
from Constant import *

__author__ = 'vinh.vo@sentifi.com'

import shelve

database = shelve.open(PATH_CACHE)
list_sentifi_categories = JSonFeeder().parser()
list_category_name = JSonFeeder().get_list_categories()
database['sc'] = list_sentifi_categories
database['cn'] = list_category_name
database.close()






