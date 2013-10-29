import sys
from twitter.TwitterStatusCrawler import TwitterStatusCrawler


from utils.IOUtils import IOUtils
from utils.PathUtils import PathUtils

def main():

    #Crawl all mentions to a People in given file
    _crawl_tweets_by_mentioning_tag()


#tag given in file
def _crawl_tweets_by_mentioning_tag():
    PATH = "D:\\SENTIFI_DATA\\mention\\"
    output_path = PATH + "output\\processing\\"

    if len(sys.argv) == 2:
        input_file_path = PATH + "input\\" + sys.argv[1]


    #Building the header for csv file
    header = ['twitter_screen_name_user','tweet_id','tweet_text','tweet_create_time','twitter_id',
                  'twitter_created','twitter_screen_name','twitter_full_name','twitter_address','twitter_email',
                  'twitter_website_url','twitter_website_full_url','twitter_description','twitter_image',
                  'twitter_image_thumbnail','twitter_followers_count','twitter_followings_count',
                  'twitter_statuses_count','twitter_listed_count']

    #Loading all filename which we have crawled in the output directory
    list_mentions_tags = IOUtils().read_first_column_in_csv(input_file_path)
    print "Total mention tags in library:", len(list_mentions_tags)

    #Get list of filename have been crawled
    list_processed_filename = PathUtils().get_list_filename(PATH + "output\\")
    print "Total mention tags has been processed", len(list_processed_filename)

    #Looking for mention tags those have NOT been crawled
    list_processed_mention = []
    for filename in list_processed_filename:
        name = filename.replace(".csv","")
        list_processed_mention.append(name)

    print list_processed_mention
    list_processing_tags = set(list_mentions_tags) - set(list_processed_mention)
    print "There have still been", len(list_processing_tags), "mentioning tag need to be crawled"

    for tag_mention in list_processing_tags:
        print "looking for who mention", tag_mention, "in their tweets"
        list_contents = TwitterStatusCrawler()._crawl_tweet_mentioning(tag_mention)
        IOUtils().save_list_to_csv(header, list_contents, output_path + tag_mention + ".csv")

def combine_mention():
    pass



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

