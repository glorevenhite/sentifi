class SentifiTwitterProfile(object):
    def __init__(self):
        self._created_at = None
        self._description = None
        self._email = None
        self._favourites_count = None
        self._followers_count = None
        self._statuses_count = None
        self._friends_count = None
        self._full_name = None
        self._website_full_url = None
        self._website_url = None
        self._listed_count = None
        self._statuses_count = None
        self._location = None
        self._image = None
        self._thumnail = None


        self._category2 = None



    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        self._created_at = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def favourites_count(self):
        return self._favourites_count

    @favourites_count.setter
    def favourites_count(self, value):
        self._favourites_count = value

    """ FOLLOWERS_COUNT """
    @property
    def followers_count(self):
        return self._followers_count

    @followers_count.setter
    def followers_count(self, value):
        self._followers_count = value

    @property
    def friends_count(self):
        return self._friends_count

    @friends_count.setter
    def friends_count(self, value):
        self._friends_count = value

    @property
    def twitter_id(self):
        return self._twitter_id

    @twitter_id.setter
    def twitter_id(self, value):
        self._twitter_id = value

    @property
    def location(self):
        return self._location
    @location.setter
    def location(self, value):
        self._location = value

    @property
    def screen_name(self):
        return self._screen_name

    @screen_name.setter
    def screen_name(self, value):
        self._screen_name = value

    @property
    def statuses_count(self):
        return self._statuses_count

    @statuses_count.setter
    def statuses_count(self, value):
        self._statuses_count = value

    @property
    def retweet_count(self):
        return self._retweet_count

    @retweet_count.setter
    def retweet_count(self, value):
        self._retweet_count = value

    @property
    def time_created(self):
        return self._time_created

    @time_created.setter
    def time_created(self, value):
        self._time_created = value

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        self._desc = value

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        self._full_name = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def website_url(self):
        return self._website_url

    @website_url.setter
    def website_url(self, value):
        self._value = value

    @property
    def website_full_url(self):
        return self._website_full_url

    @website_full_url.setter
    def website_full_url(self, value):
        self._website_full_url = value

    @property
    def category2(self):
        return self._category2

    @category2.setter
    def category2(self, value):
        self._category2 = value



    #Parse a list to an object of SentifiTwitterProfile
    def parse_to_object2(self,list):
        profile = SentifiTwitterProfile()

        profile.twitter_id = list[0]
        profile.created_at(list[1])
        profile.screen_name = list[2]
        profile.full_name(list[3])
        profile.address(list[4])
        #self.email(list[5])
        #self.website_url(list[6])
        #self.website_full_url(list[7])
        profile.description(list[8])
        #self.image(list[9])
        #self.thumnail(list[10])
        profile.followers_count(list[11])
        profile.friends_count(list[12])
        profile.statuses_count(list[13])
        #self.listed_count(list[14])

        return profile

    def parse_to_list(self):
        list = []

        list.append(self._twitter_id)
        list.append(self._screen_name)
        list.append(self._full_name)
        list.append(self._address)
        list.append(self._email)
        list.append(self._website_url)
        list.append(self._website_full_url)
        list.append(self._description)
        list.append(self._image)
        list.append(self._thumnail)
        list.append(self._followers_count)
        list.append(self._friends_count)
        list.append(self._statuses_count)
        list.append(self._listed_count)

        return list