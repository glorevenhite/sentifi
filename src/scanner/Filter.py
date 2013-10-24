from SentifiMessage import SentifiMessage
from SentifiMessage import SentifiFilter
from SentifiMessage import SentifiSearchItem
from SentifiMessage import SentifiSearchItemTagElement

from SentifiWordsBank import SentifiWordsBank

import json
import pprint

class Filter(object):
    def __init__(self, message, sentifi_search_item):
        self.message = message
        self.item = sentifi_search_item

    def apply(self):
        #get channel of message
        message_channel = self.message.channel

        #Get rule set from item which has channel is true
        ruleset = []
        if message_channel in self.item.cash_tag.channel:
            ruleset = self.item.cash_tag.get_ruleset()
        if message_channel in self.item.hash_tag.channel:
            ruleset += self.item.hash_tag.get_ruleset()
        if message_channel in self.item.mention_tag.channel:
            ruleset += self.item.mention_tag.get_ruleset()
        if message_channel in self.item.en_tag.channel:
            ruleset += self.item.en_tag.get_ruleset()
        if message_channel in self.item.de_tag.channel:
            ruleset += self.item.de_tag.get_ruleset()

        #taking list of blocked keywords. Only word with status of ON
        blacklist = []
        for word in self.item.blacklist:
            if word['status'] == 1:
                blacklist.append(word['word'])


        #for each rule in ruleset, check whether message is complied to the rule
        for rule in ruleset:
            processed_wordsbank = rule.get_wordsbank()
            tokenized_content = self._hash_content_using_wordsbank(self.message.text, processed_wordsbank)

            inclusion = rule.get_inclusion()
            exclusion= rule.exc_keywords + blacklist

            self.message.status = self._apply_filter(tokenized_content, inclusion, exclusion)
            if self.message.status == True:
                return self.message


    def _apply_filter(self, tokenized_content, inclusion, exclusion):

        #If the words
        exc =  set(tokenized_content.split(" ")) & set(exclusion)
        if len(exc) > 0:
            return False

        score = set(tokenized_content.split(" ")) & set(inclusion)

        if len(score) == len(set(inclusion)):
            return True
        else:
            return False

    def _build_wordsbank(self, wordsbank):
        #order by number of single words
        dict = {}
        for phrase in wordsbank:
            splited_words = phrase.split(" ") #spliting using space
            words_count = len(splited_words)

            #replacing space by hyphen then lowercase
            hyphen_phrase = phrase.replace(" ", "-").lower()
            dict.update({hyphen_phrase: words_count})

        #Sort dictionary order by number of single words
        sorted_dictionary = sorted(dict, key=lambda k:dict[k],reverse=True)

        return sorted_dictionary

    def _hash_content_using_wordsbank(self, raw_content, wordsbank):
        return SentifiWordsBank().tokenizer(raw_content, wordsbank).lower()

    ############################################################################

#===============================================================================
# text = "$EDEN CEO @B have just release year earnings blah blah a b"
# channel = "twitter"
# publisher = "WJS"
# message = SentifiMessage(text, channel, publisher)
#===============================================================================

#json data
#str_json_data = '{"id":"3","soid":"2","siid":"1","nb_soid":"3366","nb_siid":"2410","blacklist":[{"w":"black","status":0}],"keywords":{"tags_s":{"w":"$EDEN,$EDENN","i":"CEO, Year Earnings","e":"City","c":"Twitter"},"tags_h":{"w":"#EDEN, #EDENN","i":"CEO, Year Earnings","e":"City, Gulf","c":"Twitter"},"tags_a":{"w":"@EDEN, @EDENN","i":"ceo, year earnings","e":"city, gulf","c":"Twitter"},"keywords_en":{"w":"EDEN","i":"company","e":"gulf","c":"Twitter"},"keywords_de":{"w":"string","i":"string","e":"string","c":"string"}}}'
#json_data = json.loads(str_json_data)

#initialize
#item = SentifiSearchItem(json_data)

#filter = Filter(message, item)
#print "Before:"
#message.display()
#filter.apply()

#print "After:"
#message.display()
