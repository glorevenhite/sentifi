from utils.IOUtils import *
from utils.PathUtils import *
from utils.CrawlerUtils import CrawlerUtils

import time
import datetime
from datetime import timedelta

import json, jsonpickle
import tweepy

class TwitterUserCrawler(object):
    def __init__(self):
        OAUTH_TOKEN = '18113338-60RyLRMrW4vFxqBibn5LJPx4EAJgByRjLctM86w'
        OAUTH_SECRET = 'W9GSPl8dItl4Bk3J6dKNImcL99PSbZinkn4FREWVhUg'
        CONSUMER_KEY = 'egYRKgKOkJ2Utf06tYUFw'
        CONSUMER_SECRET = 'ezfzK9ddmwCCgBVJKCKHROYfEwX86wWYqLoVMZhicU'
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(OAUTH_TOKEN, OAUTH_SECRET)
        self._api = tweepy.API(auth)

    #CRAWLING SINGLE TWITTER USER
    def crawl_singe_user(self, screen_name):
        return self._api.get_user(screen_name = screen_name)

    #CRAWLING MANY USERS AT THE SAMETIME
    def crawl_many_users(self, list_screen_names):

        #Splitting the list of screen_name into 100 names each separated by comma. EXP: "name1, name2...,name100"
        chunks = CrawlerUtils().split_into_chunks(list_screen_names, 100)

        list_users = []
        users = None
        for chunk in chunks:
            try:
                rate_limit_json = self._api.rate_limit_status()
                remaining_hits = rate_limit_json['resources']['users']['/users/lookup']['remaining']

                print "The remaining hits for looking up user are:", remaining_hits
                users = self._api.lookup_users(screen_names = chunk)
                for u in users:
                    list_users.append(u)
            except Exception,e:
                print e
        return list_users

    def crawl_followers_of_given_user(self, name):
        ids = []
        rate_limit_json = self._api.rate_limit_status()
        remain_hits = rate_limit_json['resources']['followers']['/followers/ids']['remaining']
        print remain_hits
        if (remain_hits < 2):
            pprint.pprint(ids)
            time.sleep(15*60)

        for page in tweepy.Cursor(self._api.followers_ids, screen_name=name).pages():
            rate_limit_json = self._api.rate_limit_status()
            print len(page)
            ids.extend(page)
            #pprint.pprint(rate_limit_json['resources'])
            #pprint.pprint(rate_limit_json['resources']['followers']['/followers/ids']['remaining'])
            remain_hits = rate_limit_json['resources']['followers']['/followers/ids']['remaining']
            print remain_hits
            if (remain_hits < 2):
                pprint.pprint(ids)
                Utils.save_list_to_csv(page, filepath)
                time.sleep(15*60)
        return ids