__author__ = 'vinh.vo@sentifi.com'
import json
import pymongo
import tweepy

OAUTH_TOKEN = '18113338-60RyLRMrW4vFxqBibn5LJPx4EAJgByRjLctM86w'
OAUTH_SECRET = 'W9GSPl8dItl4Bk3J6dKNImcL99PSbZinkn4FREWVhUg'
CONSUMER_KEY = 'egYRKgKOkJ2Utf06tYUFw'
CONSUMER_SECRET = 'ezfzK9ddmwCCgBVJKCKHROYfEwX86wWYqLoVMZhicU'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_SECRET)
api = tweepy.API(auth)


class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()

        self.db = pymongo.MongoClient().test

    def on_data(self, tweet):
        json_tweet = json.loads(tweet)
        dict_tweet = dict(json_tweet)

        if 'delete' not in dict_tweet.keys():
            print json_tweet
            self.db.non_sport_tweets.insert(json.loads(tweet))

    def on_error(self, status_code):
        return True # Don't kill the stream

    def on_timeout(self):
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
sapi.sample()



