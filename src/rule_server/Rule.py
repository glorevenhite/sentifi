class Rule(object):
    def __init__(self, id):
        self.phase = ""
        self.category_name = ""
        self.rule_id = id
        self.based_words = []
        self.and_words = []
        self.not_words = []

    def set_category(self, cat_name):
        self.category_name = cat_name

    def add_new_based_word(self, based_word):
        self.based_words.append(based_word)

    def add_new_and_words(self, word):
        self.and_words.append(word)

    def add_new_not_words(self, word):
        self.not_words.append(word)

    def keywords_json(self):
        str_json = {self.rule_id: {'status': {'based': self.based_words, 'and': self.and_words, 'not': self.not_words}}}
        return str_json

    def keywords_json_2(self):
        str_json = {self.rule_id: {'status': {'and': self.and_words, 'not': self.not_words}}}
        return str_json