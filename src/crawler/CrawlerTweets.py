__author__ = 'vinh.vo@sentifi.com'

from twitter.TwitterStatusCrawler import TwitterStatusCrawler
from utils.MongoUtils import *
import json
import jsonpickle
from utils.IOUtils import IOUtils
FILE_PATH = 'D:\\sport.csv'


def crawl_tweets():
    collection = create_collection('sport_machine', 'sport_publisher')

    list_screen_name = IOUtils().read_first_column_in_csv(FILE_PATH)
    for name in list_screen_name:
        tweets = TwitterStatusCrawler().crawl_tweets_for_given_user(name)
        print 'Total:', len(tweets)
        for tw in tweets:
            json_tweet = jsonpickle.encode(tw)
            collection.insert(json.loads(json_tweet))

    print "There has been ", collection.count(), 'tweets so far'

crawl_tweets()




