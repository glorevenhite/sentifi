from Constant import *
from Client import Client
import simplejson

class TwitterProfile(object):
    def __init__(self, json_data):
        self.screen_name = json_data['screen_name']
        self.fullname = json_data['name']
        self.description = json_data['description']
        self.profile_type = None
        self.profile_group = None
        self.category1 = None
        self.category2 = None

    def set_category(self, phase, category):
        if phase == PHASE_VALUES[0]:
            self.category1 = category
        elif phase == PHASE_VALUES[1]:
            self.category2 = category
        elif phase == 'Profile Group':
            self.profile_group = category
        else:
            self.profile_type = category

    def _get_previous_stage(self, stage):
        message = {'type': 'parent', 'category_name': stage}
        client = Client()
        result = client.send(message)
        value = simplejson.loads(result)[stage]
        self.set_category('Profile Group', value)

    def display(self):
        print self.fullname,self.description, "/",self.profile_type,":",self.profile_group,":", self.category1,":",self.category2