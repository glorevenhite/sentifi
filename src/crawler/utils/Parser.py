import json, jsonpickle

class Parser(object):

    def parse_tweepy_object_to_json(self, object):
        return jsonpickle.encode(object)