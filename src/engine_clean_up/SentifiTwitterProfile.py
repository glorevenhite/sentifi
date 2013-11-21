import simplejson

from Constant import *
from SentifiField import SentifiField


class SentifiTwitterProfile(object):
    def __init__(self, data, data_type):
        if data_type == 'json':
            self.id = data['id']
            self.name = data['name']
            self.screen_name = data['screen_name']
            self.description = data['description']

        else:
            self.profile_id = data[COLUMNS[0]]
            self.id = data[COLUMNS[1]]
            self.screen_name = data[COLUMNS[2]].lower()

            if data[COLUMNS[3]] is not None:
                self.fullname = data[COLUMNS[3]].lower()
            else:
                self.fullname = ""

            if data[COLUMNS[4]] is not None:
                self.description = data[COLUMNS[4]].lower()
            else:
                self.description = ""

        self.profile_type = None
        self.profile_group = None
        self.category1 = None
        self.category2 = None

    def get_fields(self):

        # Screen Name
        snf = SentifiField()
        snf.name = TWITTER_SCREEN_NAME
        snf.channel = TWITTER
        snf.content = self.screen_name

        # Full Name
        fn = SentifiField()
        fn.name = TWITTER_FULL_NAME
        fn.channel = TWITTER
        fn.content = self.fullname

        # Description
        desc = SentifiField()
        desc.name = TWITTER_DESCRIPTION
        desc.channel = TWITTER
        desc.content = self.description

        return [snf, fn, desc]

    def to_array(self):
        list_items = []

        list_items.append(self.profile_id)
        list_items.append(self.id)
        list_items.append(self.screen_name)
        list_items.append(self.fullname)
        list_items.append(self.description)
        list_items.append(self.profile_type)
        list_items.append(self.profile_group)
        list_items.append(self.category1)
        list_items.append(self.category2)

        return list_items

    def to_array_2(self):
        list_items = []
        list_items.append(self.profile_type)
        list_items.append(self.profile_group)
        list_items.append(self.category1)
        list_items.append(self.category2)
        return list_items

    def display(self):
        print unicode(self.fullname),unicode(self.description), "/",self.profile_type,":",self.profile_group,":", self.category1,":",self.category2