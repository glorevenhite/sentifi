from utils.CrawlerUtils import CrawlerUtils
from Constant import *
import time
import datetime
from datetime import timedelta

import json, jsonpickle
import tweepy


class TwitterUserCrawler(object):
    def __init__(self):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(OAUTH_TOKEN, OAUTH_SECRET)
        self._api = tweepy.API(auth)


    #CRAWLING SINGLE TWITTER USER
    def crawl_singe_user(self, screen_name):
        return self._api.get_user(screen_name=screen_name, include_entities=True)

    def crawl_single_user_csv(self, screen_name):
        user = self._api.get_user(screen_name=screen_name)
        return user

    #CRAWLING MANY USERS AT THE SAME TIME
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
                if remaining_hits <= 2:
                    #waiting for 15 minutes
                    print "waiting..."
                    time.sleep(15*60)

                users = self._api.lookup_users(screen_names=chunk)
                for u in users:
                    list_users.append(u)
            except Exception, e:
                print e
        return list_users

    def crawl_many_users_csv(self, list_screen_names):

        #Splitting the list of screen_name into 100 names each separated by comma. EXP: "name1, name2...,name100"
        chunks = CrawlerUtils().split_into_chunks(list_screen_names, 100)
        print "crawling.."
        list_users = []
        for chunk in chunks:
            rate_limit_json = self._api.rate_limit_status()
            remaining_hits = rate_limit_json['resources']['users']['/users/lookup']['remaining']
            if remaining_hits <= 2:
                #waiting for 15 minutes
                print "waiting..."
                time.sleep(15*60)

            print "The remaining hits for looking up user are:", remaining_hits
            users = self._api.lookup_users(screen_names=chunk, )
            for u in users:
                user = []
                user.append(u.id)
                user.append(unicode(u.screen_name).encode('utf-8'))
                user.append(unicode(u.name).encode('utf-8'))
                user.append(unicode(u.location).encode('utf-8'))
                user.append(unicode(u.created_at).encode('utf-8'))
                user.append(u.url)
                user.append(unicode(u.description).encode('utf-8'))
                user.append(unicode(u.profile_image_url).encode('utf-8'))
                user.append(CrawlerUtils().rreplace(u.profile_image_url, "normal", "mini", 1))
                user.append(unicode(u.followers_count).encode('utf-8'))
                user.append(unicode(u.friends_count).encode('utf-8'))
                user.append(str(u.statuses_count))
                user.append(str(u.listed_count))

                list_users.append(user)
        return list_users

    def crawl_followers_of_given_user(self, name):
        ids = []
        rate_limit_json = self._api.rate_limit_status()
        remain_hits = rate_limit_json['resources']['followers']['/followers/ids']['remaining']
        print remain_hits
        if remain_hits < 2:

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

                #Utils.save_list_to_csv(page, filepath)
                time.sleep(15*60)
        return ids
