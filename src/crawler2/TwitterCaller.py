__author__ = 'vinh.vo@sentifi.com'
from Constant import *

from twython import Twython


class TwitterCaller(object):
    def __init__(self):
        caller = Twython(APP_KEY, APP_SECRET, oauth_version=2)
        caller = Twython(APP_KEY, access_token=ACCESS_TOKEN)
        self.caller = caller