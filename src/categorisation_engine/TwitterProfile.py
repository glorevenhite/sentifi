class TwitterProfile(object):
    def __init__(self, json_data):
        self.screen_name = json['screen_name']
        self.fullname = json['name']
        self.description = json['description']
        self.profile_type = None
        self.profile_group = None
        self.category1 = None
        self.category2 = None

    def to_json(self):
        pass

    def display(self):
        print self._f, ":", self._d, ":", self._pt