from src.engine_clean_up import JSonFeeder

__author__ = 'vinh.vo@sentifi.com'

import shelve

database = shelve.open("D:\data.gsv")
list_sentifi_categories = JSonFeeder().parser()
list_category_name = JSonFeeder().get_list_categories()
database['sc'] = list_sentifi_categories
database['cn'] = list_category_name
database.close()



