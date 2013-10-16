import pprint
import time
import datetime as dt
from datetime import timedelta

import tweepy

from twitter.TwitterCrawler import TwitterCrawler

from utils import *

def main():
    """
        CRAWL ALL MENTIONS TO GIVEN PEOPLE.
        THE LIST OF GIVEN NAME GIVEN IN THE FILE_PATH
    """
    _crawl_tweet_mentioning()


def _crawl_tweet_mentioning():
    PATH = "D:\\"
    input_file_path = "mention_text.csv"
    output_path = "mention_text_result.csv"

    TwitterCrawler().crawl_tweet_mentioning_from_file(file_path)

if __name__ == "__main__":
    main()

