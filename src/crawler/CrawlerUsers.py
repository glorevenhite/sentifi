from TwitterUserCrawler import TwitterUserCrawler
from utils.CrawlerUtils import *
from utils.IOUtils import IOUtils
from utils.Parser import Parser
import json
import sys
from Constant import *


def main():
    if len(sys.argv) == 3:
        input_file_name = PROFILES_INPUT + sys.argv[2]

        if sys.argv[1] == 'json':
            list_users = crawl_users_by_list_screen_names()
            for user in list_users:
                raw_json_user = Parser().parse_tweepy_object_to_json(user)
                json_obj = json.loads(raw_json_user)

                file_name = json_obj['screen_name'] + ".json"

                IOUtils().save_json_data_to_file(raw_json_user, file_name, PROFILES_OUTPUT)
        elif sys.argv[1] == 'csv':
            list_users = crawl_users_by_list_screen_names_csv(input_file_name)
            IOUtils().save_list_to_csv(None, list_users, PROFILES_OUTPUT + "result.csv")
    else:
        print "PLease enter the type of export file and file_path:"


def crawl_users_by_list_screen_names(input_file_name):

    print "Path to the file containing screen names", input_file_name

    list_screen_names = CrawlerUtils().read_screen_names_from_csv_file(input_file_name)
    print len(list_screen_names), "twitter users are going to be crawled..."

    list_users = TwitterUserCrawler().crawl_many_users(list_screen_names)

    return list_users


def crawl_users_by_list_screen_names_csv(file_name):

    list_screen_names = CrawlerUtils().read_screen_names_from_csv_file(file_name)
    print len(list_screen_names), "twitter users are going to be crawled..."

    list_users = TwitterUserCrawler().crawl_many_users_csv(list_screen_names)

    return list_users


if __name__ == "__main__":
    main()

