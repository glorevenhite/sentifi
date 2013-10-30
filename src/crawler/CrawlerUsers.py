import sys

from twitter.TwitterUserCrawler import TwitterUserCrawler

from utils.CrawlerUtils import *
from utils.IOUtils import IOUtils
from Config import Configuration
from utils.Parser import Parser
import json

def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == 'json':
            list_users = crawl_users_by_list_screen_names()
            for user in list_users:
                raw_json_user = Parser().parse_tweepy_object_to_json(user)
                json_obj = json.loads(raw_json_user)

                file_name = json_obj['screen_name'] + ".json"

                IOUtils().save_json_data_to_file(raw_json_user, file_name, "D:\\")
    else:
        print "PLease enter the PATH"


def crawl_users_by_list_screen_names():
    FILE_PATH = Configuration().HOME_PATH + "user\\input\\screen_names.csv"
    print "Path to the file containing screen names", FILE_PATH

    list_screen_names = CrawlerUtils().read_screen_names_from_csv_file(FILE_PATH)
    print len(list_screen_names), "twitter users are going to be crawled..."

    list_users = TwitterUserCrawler().crawl_many_users(list_screen_names)

    return list_users

if __name__ == "__main__":
    main()

