"""
Created on Aug 30, 2013

__author__ = 'nadan'
"""

import time
import datetime
import pycurl
import urllib
import json
import oauth2 as oauth


class TwitterStream():

    def __init__(self, stream_name, timeout=False):

        # Daemon properties
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_timeout = 5
        self.pidfile_path = stream_name

        # Streaming properties
        self.oauth_token = None
        self.oauth_consumer = None
        self.post_params = {
            'stall_warnings': 'true',
            'follow': ''
        }  # a dict: {'stall_warning':true, 'follow': <publisher string list comma separator>}
        self.collection = None
        self.raw_collection = None
        self.logger = None
        self.api_end_point = 'https://stream.twitter.com/1.1/statuses/filter.json'

        # Connection properties
        self.conn = None
        self.buffer = ''
        self.timeout = timeout
        self.user_agent = 'TwitterStream 1.0'

    def setup_connection(self):
        """ Create persistent HTTP connection to Streaming API endpoint using cURL.
        """
        if self.conn:
            self.conn.close()
            self.buffer = ''
        self.conn = pycurl.Curl()
        # Restart connection if less than 1 byte/s is received during "timeout" seconds
        if isinstance(self.timeout, int):
            self.conn.setopt(pycurl.LOW_SPEED_LIMIT, 1)
            self.conn.setopt(pycurl.LOW_SPEED_TIME, self.timeout)
        self.conn.setopt(pycurl.URL, self.api_end_point)
        self.conn.setopt(pycurl.USERAGENT, self.user_agent)
        # Using gzip is optional but saves us bandwidth.
        self.conn.setopt(pycurl.ENCODING, 'deflate, gzip')
        # for post method only
        self.conn.setopt(pycurl.POST, 1)
        self.conn.setopt(pycurl.POSTFIELDS, urllib.urlencode(self.post_params))
        self.conn.setopt(pycurl.HTTPHEADER, ['Host: stream.twitter.com',
                                             'Authorization: %s' % self.get_oauth_header()])
        # self.handle_tweet is the method that are called when new tweets arrive
        self.conn.setopt(pycurl.WRITEFUNCTION, self.handle_tweet)

    def get_oauth_header(self):
        """ Create and return OAuth header.
        """
        params = {'oauth_version': '1.0',
                  'oauth_nonce': oauth.generate_nonce(),
                  'oauth_timestamp': int(time.time())}
        #req = oauth.Request(method='POST', parameters=params, url='%s?%s' % (API_ENDPOINT_SAMPLE_URL,
        #                                                                     urllib.urlencode(POST_PARAMS)))
        req = oauth.Request(method='POST', 
                            parameters=params, 
                            url='%s?%s' % (self.api_end_point, urllib.urlencode(self.post_params)))
        req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), 
                         self.oauth_consumer, self.oauth_token)
        return req.to_header()['Authorization'].encode('utf-8')

    def run(self):
        """ Start listening to Streaming endpoint.
        Handle exceptions according to Twitter's recommendations.
        """
        back_off_network_error = 0.25
        back_off_http_error = 5
        back_off_rate_limit = 60

        while True:
            self.setup_connection()
            try:
                self.conn.perform()
            except:
                # Network error, use linear back off up to 16 seconds
                self.logger.error('Error: ' + self.conn.errstr())
                self.logger.error('Waiting ' + str(back_off_network_error)
                                  + ' seconds before trying again (back off linearly)')
                time.sleep(back_off_network_error)
                back_off_network_error = min(back_off_network_error + 1, 16)
                #write to file, for testing only
                continue
            # HTTP Error
            sc = self.conn.getinfo(pycurl.HTTP_CODE)
            if sc == 420:
                # Rate limit, use exponential back off starting with 1 minute and double each attempt
                self.logger.critical('Rate limit, waiting ' + str(back_off_rate_limit) + ' seconds')
                time.sleep(back_off_rate_limit)
                back_off_rate_limit *= 2
            else:
                # HTTP error, use exponential back off up to 320 seconds
                self.logger.error('HTTP error ' + str(sc) + ': ' + self.conn.errstr()) 
                self.logger.error('Waiting ' + str(back_off_http_error) + ' seconds')
                time.sleep(back_off_http_error)
                back_off_http_error = min(back_off_http_error * 2, 320)

    def handle_tweet(self, data):
        """ This method is called when data is received through Streaming endpoint.
        """
        self.buffer += data
        if data.endswith('\r\n') and self.buffer.strip():
            # complete message received
            try:
                message = json.loads(self.buffer)
            except ValueError:
                self.logger.error('Error data: ' + data)
            self.buffer = ''
            if message.get('limit'):
                self.logger.warn('Rate limiting caused us to miss ' 
                                 + message['limit'].get('track') + ' tweets')
            elif message.get('disconnect'):
                self.logger.critical('Got disconnect: ' + message['disconnect'].get('reason'))
                raise Exception('Got disconnect: ' + message['disconnect'].get('reason'))
            elif message.get('warning'):
                self.logger.warn('Got warning: ' + message['warning'].get('message'))
            elif message.get('delete'):
                pass
            elif message.get('scrub_geo'):
                pass
            elif message.get('status_withheld'):
                pass
            elif message.get('user_withheld'):
                pass
            else:
                try:
                    new_message = {
                        'message_id': message['id_str'],
                        'user_screen_name': message['user']['screen_name'],
                        'user_id': message['user']['id_str'],
                        'text': message['text'],
                        'created_at': datetime.datetime.strptime(message.get('created_at', datetime.datetime.utcnow()),
                                                                 '%a %b %d %H:%M:%S +0000 %Y'),
                        'timestamp': datetime.datetime.utcnow(),
                        'lang': message['lang']
                    }
                    self.collection.insert(new_message)
                except KeyError:
                    self.logger.warn('KeyError')
                self.raw_collection.insert(message)