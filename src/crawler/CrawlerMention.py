import sys
from twitter.TwitterStatusCrawler import TwitterStatusCrawler
from Constant import *
from utils.IOUtils import IOUtils
from utils.PathUtils import PathUtils

def main():

    #Crawl all mentions to a People in given file
    _crawl_tweets_by_mentioning_tag()


def _crawl_tweets_by_mentioning_tag():
    input_file_path = ""

    #taking the 3rd argument as the file_name.
    if len(sys.argv) == 2:
        input_file_path = MENTION_INPUT + sys.argv[1]

    list_processing_tags = _get_list_mention_tags_need_to_be_processed(input_file_path)

    for tag_mention in list_processing_tags:
        print "looking for who mention", tag_mention, "in their tweets"
        list_contents = TwitterStatusCrawler().crawl_tweet_mentioning(tag_mention)
        IOUtils().save_list_to_csv(MENTION_HEADER, list_contents, MENTION_OUTPUT_PATH + tag_mention + ".csv")


def _get_list_mention_tags_need_to_be_processed(input_file_path):

    #Get all tags need to be processed
    list_mentions_tags = IOUtils().read_first_column_in_csv(input_file_path)
    print "Total mention tags in library:", len(list_mentions_tags)

    #Get list of filename have been crawled
    list_processed_filename = PathUtils().get_list_filename(MENTION_OUTPUT_PATH)
    print "Total mention tags has been processed", len(list_processed_filename)

    #Looking for mention tags those have NOT been crawled
    list_processed_mention = []
    for filename in list_processed_filename:
        name = filename.replace(".csv", "")
        list_processed_mention.append(name)

    print list_processed_mention

    list_processing_tags = set(list_mentions_tags) - set(list_processed_mention)
    print "There have still been", len(list_processing_tags), "mentioning tag need to be crawled"

    return list_processing_tags

if __name__ == "__main__":
    main()