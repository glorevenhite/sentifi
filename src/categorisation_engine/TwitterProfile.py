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
        if phase.upper() == PHASE_VALUES[0]:
            self.profile_type = category
        elif phase.upper() == PHASE_VALUES[1]:
            self.profile_group = category
        elif phase.upper() == PHASE_VALUES[2]:
            self.category1 = category
        else:
            self.category2 = category

    def _get_previous_stage(self, stage):
        message = {'type': 'parent', 'category_name': stage}
        client = Client()
        result = client.send(message)
        value = simplejson.loads(result)[stage]
        self.set_category('Profile Group', value)

    def display(self):
        print self.fullname,self.description, "/",self.profile_type,":",self.profile_group,":", self.category1,":",self.category2