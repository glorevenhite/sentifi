class TwitterProfile(object):
    def __init__(self, fullname, description):
        self._f = fullname
        self._d = description
        self._pt = None
        self._pg = None
        self._cat1 = None
        self._cat2 = None

    @property
    def fullname(self):
        return self._f

    @fullname.setter
    def fullname(self, value):
        self._f = value

    @property
    def description(self):
        return self._d

    @description.setter
    def description(self, value):
        self._d = value

    @property
    def profile_type(self):
        return self._pt

    @profile_type.setter
    def profile_type(self, value):
        self._pt = value

    @property
    def publisher_group(self):
        return self._pg

    @property
    def category1(self):
        return self._cat1

    @category1.setter
    def category1(self, value):
        self._cat1 = value

    @property
    def category2(self):
        return self.category_2()

    @category2.setter
    def category2(self, value):
        self._cat2 = value

    def convert_to_list(self):
        list = []
        list.append(self._f)
        list.append(self._d)
        list.append(self._pt)
        list.append(self._pg)
        list.append(self._cat1)
        list.append(self._cat2)
        return list

    def display(self):
        print self._f, ":", self._d, ":", self._pt