from utils.IOUtils import *
from utils.PathUtils import *

import time
import datetime
from datetime import timedelta

import json, jsonpickle
import tweepy

class TwitterCrawler(object):
    def __init__(self):
        OAUTH_TOKEN = '18113338-60RyLRMrW4vFxqBibn5LJPx4EAJgByRjLctM86w'
        OAUTH_SECRET = 'W9GSPl8dItl4Bk3J6dKNImcL99PSbZinkn4FREWVhUg'
        CONSUMER_KEY = 'egYRKgKOkJ2Utf06tYUFw'
        CONSUMER_SECRET = 'ezfzK9ddmwCCgBVJKCKHROYfEwX86wWYqLoVMZhicU'
        auth =tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(OAUTH_TOKEN, OAUTH_SECRET)
        self._api = tweepy.API(auth)

    # Return data in tweepy format
    def crawl_single_user(self, screen_name):
        user = self._api.get_user(screen_name = screen_name)

        pickled = jsonpickle.encode(user)

        return pickled
        #print(json.dumps(json.loads(pickled), indent=4, sort_keys=True))
    #def crawl_single_user(self, screen_name):


print TwitterCrawler().crawl_single_user('glorevenhite')

