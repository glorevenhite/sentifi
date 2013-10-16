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
        return jsonpickle.encode(self._api.get_user(screen_name = screen_name))

    def _crawl_tweet_mentioning(self, mention_text):
        tweets = []
        header = ['twitter_screen_name_user','tweet_id','tweet_text','tweet_create_time','twitter_id',
                  'twitter_screen_name','twitter_full_name','twitter_address','twitter_email',
                  'twitter_website_url','twitter_website_full_url','twitter_description','twitter_image',
                  'twitter_image_thumbnail','twitter_followers_count','twitter_followings_count',
                  'twitter_statuses_count','twitter_listed_count']
        tweets.append(header)

        pages = tweepy.Cursor(self._api.search, q=mention_text, count = 100).pages()
        for page in pages:
            rate_limit_json = self._api.rate_limit_status()
            remain_hits = rate_limit_json['resources']['search']['/search/tweets']['remaining']
            print "Remain hits:", remain_hits
            print len(page)

            for tweet in page:
                tw = []

                tw.append(unicode(mention_text.replace("@","")).encode('utf-8'))

                tw.append(tweet.id)
                tw.append(unicode(tweet.text).encode('utf-8'))
                tw.append(tweet.created_at)
                tw.append(unicode(str(tweet.user.id)).encode('utf-8'))
                tw.append(unicode(tweet.user.screen_name).encode('utf-8'))
                tw.append(unicode(tweet.user.name).encode('utf-8'))
                tw.append(unicode(tweet.user.location).encode('utf-8'))
                tw.append("")
                tw.append(unicode(tweet.user.url).encode('utf-8'))
                tw.append(unicode(tweet.user.url).encode('utf-8'))
                tw.append(unicode(tweet.user.description).encode('utf-8'))
                tw.append(unicode(tweet.user.profile_image_url).encode('utf-8'))
                tw.append(Utils().rreplace(tweet.user.profile_image_url,"normal", "mini", 1))
                tw.append(unicode(tweet.user.followers_count).encode('utf-8'))
                tw.append(unicode(tweet.user.friends_count).encode('utf-8'))
                tw.append(str(tweet.user.statuses_count))
                tw.append(str(tweet.user.listed_count))
                #tw.append(str(tweet.user.favourites_count))
                tweets.append(tw)

            print "Total mentions so far:", len(tweets)
            if (len(tweets) >= 50000): #reach limit of max tweet can be retrieved
                return tweets
            if (remain_hits <= 2):
                time.sleep(15*60) #waiting for 15 minutes

            if (len(tweets) == 3200): #reach limit of max tweet can be retrieved
                return tweets

        return tweets



print TwitterCrawler().crawl_single_user('glorevenhite')

