from utils.PathUtils import *
from utils.CrawlerUtils import CrawlerUtils
from Config.Config import Configuration

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
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(OAUTH_TOKEN, OAUTH_SECRET)
        self._api = tweepy.API(auth)

    #CRAWLING SINGLE TWITTER USER
    def crawl_singe_user(self, screen_name):
        return self._api.get_user(screen_name = screen_name)

    #CRAWLING MANY USERS AT THE SAMETIME
    def crawl_many_users(self, list_screen_names):

        #Splitting the list of screen_name into 100 names each
        chunks = CrawlerUtils().split_into_chunks(list_screen_names, 100)

        list_users = []
        users = None
        for chunk in chunks:
            try:
                users = self._api.lookup_users(screen_names = chunk)
                for u in users:
                    list_users.append(u)
            except Exception,e:
                print e, chunk

        return list_users

    #CRAWING TWEETS THAT MENTION TO
    def crawl_tweet_mentioning(self, mention_text):
        tweets = []

        pages = tweepy.Cursor(self._api.search, q=mention_text, count = 100).pages()
        for page in pages:
            rate_limit_json = self._api.rate_limit_status()
            remain_hits = rate_limit_json['resources']['search']['/search/tweets']['remaining']
            print "Remain hits:", remain_hits

            for tweet in page:
                tweepy.user = tweet.user
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
                tw.append(CrawlerUtils().rreplace(tweet.user.profile_image_url,"normal", "mini", 1))
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

    #Accept a file contains a list of mention, then export to files
    def crawl_tweet_mentioning_from_file(self, input_file_path, output_path):
        screen_names = []

        screen_names = Utils().read_screen_name_from_csv(file_path)

        for name in screen_names:
            tweets = self._crawl_tweet_mentioning(name)
            Utils().save_list_to_csv(tweets, PATH + name + ".csv")

    #Crawler lastest tweets for given user (maximum 3200tweets/user)
    def crawl_tweets_for_given_user(self, screen_name):
        tweets = []

        try:
            pages = tweepy.Cursor(self._api.user_timeline, screen_name = screen_name, count = 200).pages()

            for page in pages:
                rate_limit_json = self._api.rate_limit_status()
                remain_hits = rate_limit_json['resources']['statuses']['/statuses/user_timeline']['remaining']
                print "Remain hits:", remain_hits

                print len(page)

                for tweet in page:
                    tweets.append(tweet)

                print "Total tweets of current user so far", len(tweets)

                if (remain_hits <= 2):
                    time.sleep(15*60) #waiting for 15 minutes

                if (len(tweets) == 3200): #reach limit of max tweet can be retrieved
                    return tweets
        except:
            pass
        return tweets

    def craw_followers(self, name):
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
            remain_hits = rate_limit_json['resources']['followers']['/followers/ids']['']
            print remain_hits
            if (remain_hits < 2):
                pprint.pprint(ids)
                Utils.save_list_to_csv(page, filepath)
                time.sleep(15*60)
        return ids

    def _crawl_tweet_mentioning(self, mention_text):
        tweets = []
        """header = ['twitter_screen_name_user','tweet_id','tweet_text','tweet_create_time','twitter_id',
                  'twitter_screen_name','twitter_full_name','twitter_address','twitter_email',
                  'twitter_website_url','twitter_website_full_url','twitter_description','twitter_image',
                  'twitter_image_thumbnail','twitter_followers_count','twitter_followings_count',
                  'twitter_statuses_count','twitter_listed_count']
        tweets.append(header)"""

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
                tw.append(CrawlerUtils().rreplace(tweet.user.profile_image_url,"normal", "mini", 1))
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

    def crawl_tweets_by_mentioning_tag_from_file(self, mention_text):
        tweets = []
        print "Search:",mention_text

        pages = tweepy.Cursor(self._api.search, q=mention_text, count = 100).pages()

        for page in pages:
            rate_limit_json = self._api.rate_limit_status()
            remain_hits = rate_limit_json['resources']['search']['/search/tweets']['remaining']
            print "Remain hits:", remain_hits

            for tweet in page:
                tweets.append(tweet)

            print "Total mentions so far:", len(tweets)
            if (len(tweets) >= 3000): #reach limit of max tweet can be retrieved
                return tweets
            if (remain_hits <= 2):
                time.sleep(15*60) #waiting for 15 minutes

            if (len(tweets) == 3200): #reach limit of max tweet can be retrieved
                return tweets

        return tweets


#print TwitterCrawler().crawl_single_user('glorevenhite')

