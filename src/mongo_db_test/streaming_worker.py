__author__ = 'nadan'


import sys
import logging
import logging.handlers
import oauth2 as oauth
from os import getcwd
import daemon
from pymongo import MongoClient
from twitterstream import TwitterStream


def get_publisher_list(mongo_client, stream_name):
    publisher_table = mongo_client['sentifi']['publisher']
    cursor = publisher_table.find({'has_twitter_info': True, 'twitter_streaming_info.active': False},
                                  {'twitter_info.twitter_id': 1, '_id': 0}).limit(5000)

    publisher_list = []
    for publisher in cursor:
        publisher_list.append(publisher['twitter_info']['twitter_id'])

    for publisher_id in publisher_list:
        publisher_table.update({'twitter_info.twitter_id': publisher_id},
                               {'$set': {'twitter_streaming_info.active': True,
                                         'twitter_streaming_info.stream_name': stream_name}}, upsert=False, multi=True)
                               # {'upsert': False}, {'multi': True})

    return publisher_list


def get_twitter_key(mongo_client, stream_name):
    key_table = mongo_client['sentifi']['twitter_key']
    key_info = key_table.find_one({'active': False},
                                  {'consumer_key': 1, 'consumer_secret': 1,
                                   'access_token_key': 1, 'access_token_secret': 1})

    if key_info:
        key_table.update({'_id': key_info['_id']},
                         {'$set': {'active': True, 'stream_name': stream_name}})
    else:
        print 'There is no available key'
        return

    key_info.pop('_id')

    return key_info


def free_publisher(mongo_client, stream_name):
    publisher_table = mongo_client['sentifi']['publisher']
    publisher_table.update({'twitter_streaming_info.stream_name': stream_name},
                           {'$set': {'twitter_streaming_info':
                                    {'active': False, 'stream_name': ''}}}, upsert=False, multi=True)


def free_key(mongo_client, stream_name):
    key_table = mongo_client['sentifi']['twitter_key']
    key_table.update({'stream_name': stream_name},
                     {'$set': {'active': False, 'stream_name': ''}}, upsert=False, multi=True)


if __name__ == '__main__':

    # Create rotate logger handler
    logger = logging.getLogger(sys.argv[2])
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    rtlBaseFile = '../log/stream/stream.log'
    handler = logging.handlers.RotatingFileHandler(rtlBaseFile, maxBytes=1024*1024*4, backupCount=9)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    stream = TwitterStream(getcwd() + '/pid/' + sys.argv[2] + '.pid')  # must be an absolute path here
    if len(sys.argv) == 3:
        if 'start' == sys.argv[1]:

            client = MongoClient('localhost', 27017)

            print 'Setting things up'

            twitter_key = get_twitter_key(client, sys.argv[2])
            stream.oauth_token = oauth.Token(key=twitter_key['access_token_key'],
                                             secret=twitter_key['access_token_secret'])
            stream.oauth_consumer = oauth.Consumer(key=twitter_key['consumer_key'],
                                                   secret=twitter_key['consumer_secret'])
            print 'Key OK'

            # publisher_list must be a string
            stream.post_params['follow'] = ', '.join(get_publisher_list(client, sys.argv[2]))
            print 'Publisher OK'

            stream.raw_collection = client['sentifi']['twitter_stream']
            stream.collection = client['sentifi']['twitter_message']
            print 'DB OK'

            stream.logger = logger
            print 'Log OK'

            print 'Start!'
            daemon_runner = daemon.runner.DaemonRunner(stream)
            daemon_runner.daemon_context.files_preserve = [handler.stream]
            daemon_runner.do_action()
        elif 'stop' == sys.argv[1]:
            client = MongoClient('localhost', 27017)
            print 'Stopping'

            free_key(client, sys.argv[2])
            print 'Free Key Done'

            free_publisher(client, sys.argv[2])
            print 'Free Publisher Done'

            daemon_runner = daemon.runner.DaemonRunner(stream)
            daemon_runner.do_action()
            print 'Stop Done'
        elif 'restart' == sys.argv[1]:
            pass
            # still not know how to do restart
            # daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)