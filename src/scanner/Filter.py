from SentifiMessage import SentifiMessage
from SentifiMessage import SentifiFilter
from SentifiWordsBank import SentifiWordsBank

class Filter(object):
    def __init__(self, json_data):
        self.json_data = json_data

    def filter(self, message, filters):
        cash_filter = filters[0]
        hash_filter = filters[1]
        mention_filter = filters[2]
        en_filter = filters[3]
        de_filter = filters[4]

        #Creating bank of vocabulary used
        wordsbank = list(set(cash_filter.wordsbank) |
                         set(hash_filter.wordsbank) |
                         set(mention_filter.wordsbank) |
                         set(en_filter.wordsbank) |
                         set(de_filter.wordsbank))

        processed_wordsbank = self._build_wordsbank(wordsbank)
        tokenized_content = self._hash_content_using_wordsbank(message.text, processed_wordsbank)

        #apply filter
        message.status = self._apply_filter(tokenized_content, processed_wordsbank)
        message.display()

    def _apply_filter(self, tokenized_content, processed_wordsbank):
        print tokenized_content
        score = set(tokenized_content.split(" ")) & set(processed_wordsbank)

        if (len(score) > 0):
            return True



    def _build_wordsbank(self, wordsbank):
        #order by number of single words
        dict = {}
        for phrase in wordsbank:
            splited_words = phrase.split(" ") #spliting using space
            words_count = len(splited_words)

            #replacing space by hyphen then lowercase
            hyphen_phrase = phrase.replace(" ", "-").lower()
            dict.update({hyphen_phrase: words_count})

        sorted_dictionary = sorted(dict, key=lambda k:dict[k],reverse=True)

        return sorted_dictionary

    def _hash_content_using_wordsbank(self, raw_content, wordsbank):

        return SentifiWordsBank().tokenizer(raw_content, wordsbank)







    ############################################################################

text = "@ADEN @B have just release year earning blah blah a b"
channel = "twitter"
publisher = "WJS"
message = SentifiMessage(text, channel, publisher)

json_data = None

s_filter = SentifiFilter(['$ADEN'], ['CEO','Year Earning'],['GULF','city'])
h_filter = SentifiFilter(['$ADEN'], ['CEO','Earning'],['GULF','city'])
a_filter = SentifiFilter(['$ADEN'], ['CEO','Earning'],['GULF','city'])
en_filter = SentifiFilter(['$ADEN'], ['CEO','Earning'],['GULF','city'])
de_filter = SentifiFilter(['$ADEN'], ['CEO','Earning'],['GULF','city'])

filters = [s_filter, h_filter, a_filter, en_filter, de_filter]


Filter(json_data).filter(message, filters)