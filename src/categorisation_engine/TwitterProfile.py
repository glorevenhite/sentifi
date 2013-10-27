from Constant import *

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
        elif phase == PHASE_VALUES[3]:
            self.profile_type = category
        else:
            self.profile_group = category

    def display(self):
        print self.fullname,self.description,self.profile_type,self.profile_group,":", self.category1,self.category2