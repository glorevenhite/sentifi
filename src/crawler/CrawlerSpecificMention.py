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
    tag_mention = ""
    if len(sys.argv) == 2:
        tag_mention = sys.argv[1]


    #Building the header for csv file
    header = ['twitter_screen_name_user','tweet_id','tweet_text','tweet_create_time','twitter_id',
                  'twitter_created','twitter_screen_name','twitter_full_name','twitter_address','twitter_email',
                  'twitter_website_url','twitter_website_full_url','twitter_description','twitter_image',
                  'twitter_image_thumbnail','twitter_followers_count','twitter_followings_count',
                  'twitter_statuses_count','twitter_listed_count']

    list_contents = TwitterStatusCrawler()._crawl_tweet_mentioning(tag_mention)
    print len(list_contents)
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

