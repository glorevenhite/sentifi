import pprint
import time
import datetime as dt
from datetime import timedelta

from Config import *

import tweepy

from twitter.TwitterCrawler import TwitterCrawler
from utils.CrawlerUtils import *

from utils.IOUtils import IOUtils
from utils.PathUtils import PathUtils

def main():
    PATH = "D:\\online-cloud\\Dropbox\\SENTIFI\\"

    #Crawl all mentions to a People in given file
    _crawl_tweets_by_mentioning_tag()

    #
    #crawl_users_by_list_screen_names()

#tag given in file
def _crawl_tweets_by_mentioning_tag():
    PATH = "D:\\SENTIFI_DATA\\mention_csv\\"
    input_file_path = PATH + "input\\mention.csv"
    output_path = PATH + "output\\processing\\"

    #Building the header for csv file
    header = ['twitter_screen_name_user','tweet_id','tweet_text','tweet_create_time','twitter_id',
                  'twitter_created','twitter_screen_name','twitter_full_name','twitter_address','twitter_email',
                  'twitter_website_url','twitter_website_full_url','twitter_description','twitter_image',
                  'twitter_image_thumbnail','twitter_followers_count','twitter_followings_count',
                  'twitter_statuses_count','twitter_listed_count']

    #Loading all filename which we have crawled in the output directory
    list_mentions = IOUtils().read_list_from_csv(input_file_path)
    list_mention_tags = []

    for tag in list_mentions:
        list_mention_tags.append(tag[0])

    print list_mention_tags

    print "Total mention tags in library:", len(list_mention_tags)

    list_processed_filename = PathUtils().get_list_filename(PATH + "output\\")

    print "Total mention tags has been processed", len(list_processed_filename)

    list_processing_mention = []
    for filename in list_processed_filename:
        name = filename.replace(".csv","")
        list_processing_mention.append(name)
        #if name not in list_mention_tags:
         #   list_processing_mention.append(name)


    print list_processing_mention
    list = set(list_mention_tags) - set(list_processing_mention)
    print len(list)

    print "Total mention tags:", len(list_processing_mention)

    for tag_mention in list:
        print "looking for who mention #", tag_mention, "in their tweets"
        list_contents = TwitterCrawler()._crawl_tweet_mentioning(tag_mention)
        IOUtils().save_list_to_csv(header, list_contents, output_path + tag_mention + ".csv")


def crawl_users_by_list_screen_names():
    FILE_PATH = Config().PATH + "data\\screen_names.csv"

    list_screen_names = CrawlerUtils().read_screen_names_from_csv_file(FILE_PATH)
    print len(list_screen_names)

    list_users = TwitterCrawler().crawl_many_users(list_screen_names)

    print len(list_users)

def _crawl_tweets_mention_text_from_file(file_path):
    FILE_PATH = Co
    list_mention_text = "adf"

def count_mention_per_tag(mention_text):
    PATH = "D:\\SENTIFI_DATA\\mention_csv\\"

    #loading file
    list = PathUtils().get_list_filename(PATH)

    #list_content
    #list_contents =
    #reading each file


    #count

    #pair

if __name__ == "__main__":
    main()

