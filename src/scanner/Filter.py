from SentifiMessage import SentifiMessage

class Filter(object):
    def __init__(self, json_data):
        self.json_data = json_data

    def filter(self, message):
        keywords = self._get_keywords_from_json(self.json_data)
        inclusion = self._get_inclusion_keywords(self.json_data)
        exclusion = self._get_exclusion_keywords(self.json_data)

        wordsbank = list(set(keywords) | set(inclusion) | set(exclusion))

        print wordsbank


        pass

    ############################################################################
    def _get_keywords_from_json(self, json_data):
        return ['$A','$B','$C']

    def _get_inclusion_keywords(self, json_data):
        return ['a','b','c']

    def _get_exclusion_keywords(self, json_data):
        return ['x', 'y','z']

    def _get_black_list_keywords(self, json_data):
        return ['w']

text = "@A @B is blah blah a b"
channel = "twitter"
publisher = "WJS"
message = SentifiMessage(text, channel, publisher)

Filter().filter(message)