class TwitterProfile(object):
    def __init__(self, json_data):
        self.screen_name = json_data['screen_name']
        self.fullname = json_data['name']
        self.description = json_data['description']
        self.profile_type = None
        self.profile_group = None
        self.category1 = None
        self.category2 = None

    def to_json(self):
        pass

    def display(self):
        print self._f, ":", self._d, ":", self._pt