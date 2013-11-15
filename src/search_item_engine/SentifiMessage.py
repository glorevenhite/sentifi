from Rule import Rule
import json

class SentifiMessage(object):
    def __init__(self, json_data):
        self.id = json_data['id']
        self.soid = json_data['soid']
        self.text = json_data['text']
        self.channel = json_data['channel']
        self.publisher = json_data['publisher']
        self.status = False


    def display(self):
        print self.text, self.publisher, self.channel, self.status

    def get_json(self):
        json_data = {"id":self.id,"soid":self.soid,"text":self.text, "channel":self.channel, "publisher":self.publisher, "status":self.status}
        return json.dumps(json_data)

#################################################################################################333
class SentifiSearchItem(object):
    def __init__(self, json_data):
        self.soid = json_data['soid']

        s_based_words = json_data['keywords'][0]['word'].split(",")
        s_inclusion = json_data['keywords'][0]['include'].split(",")
        s_exclusion = json_data['keywords'][0]['exclude'].split(",")
        s_channel = json_data['keywords'][0]['channel'].split(",")
        self.cash_tag = SentifiSearchItemTagElement('$tag',s_based_words, s_inclusion, s_exclusion, s_channel)

        h_based_words = json_data['keywords'][1]['word'].split(",")
        h_inclusion = json_data['keywords'][1]['include'].split(",")
        h_exclusion = json_data['keywords'][1]['exclude'].split(",")
        h_channel = json_data['keywords'][1]['channel'].split(",")
        self.hash_tag = SentifiSearchItemTagElement('#tag',h_based_words, h_inclusion, h_exclusion, h_channel)

        a_based_words = json_data['keywords'][2]['word'].split(",")
        a_inclusion = json_data['keywords'][2]['include'].split(",")
        a_exclusion = json_data['keywords'][2]['exclude'].split(",")
        a_channel = json_data['keywords'][2]['channel'].split(",")
        self.mention_tag = SentifiSearchItemTagElement('@tag',a_based_words, a_inclusion, a_exclusion, a_channel)

        en_based_words = json_data['keywords'][3]['word'].split(",")
        en_inclusion = json_data['keywords'][3]['include'].split(",")
        en_exclusion = json_data['keywords'][3]['exclude'].split(",")
        en_channel = json_data['keywords'][3]['channel'].split(",")
        self.en_tag = SentifiSearchItemTagElement('en',en_based_words, en_inclusion, en_exclusion, en_channel)

        de_based_words = json_data['keywords'][4]['word'].split(",")
        de_inclusion = json_data['keywords'][4]['include'].split(",")
        de_exclusion = json_data['keywords'][4]['exclude'].split(",")
        de_channel = json_data['keywords'][4]['channel'].split(",")
        self.de_tag = SentifiSearchItemTagElement('de',de_based_words, de_inclusion, de_exclusion, de_channel)

        #Blacklists
        self.blacklist = json_data['blacklists']

    def display(self):
        print self.cash_tag
        print self.hash_tag
        print self.mention_tag

####################################################################################################3
class SentifiSearchItemTagElement(object):
    def __init__(self, name, based_words, inclusion, exclusion, channel):
        self.name = name
        self.based_words = based_words
        self.inclusion = inclusion
        self.exclusion = exclusion
        self.channel = channel
        self.wordsbank = list(set(based_words) | set(inclusion) | set(exclusion))

    def get_ruleset(self):
        ruleset = []

        pair_inclusion = []
        for bw in self.based_words:
            for ic in self.inclusion:
                pair = [bw, ic]
                pair_inclusion.append(pair)

        #Combine each pair in inclusion_list with exclusion_list
        for pair in pair_inclusion:
            for ew in self.exclusion:
                rule = Rule()
                rule.inc_keywords = pair
                rule.exc_keywords.append(ew)

                ruleset.append(rule)

        return ruleset

    def display(self):
        pass



########################################################################################33
class SentifiFilter(object):
    def __init__(self, based_words, inclusion, exclusion):
        self.based_words = based_words
        self.inclusion = inclusion
        self.exclusion = exclusion
        self.wordsbank = list(set(based_words) | set(inclusion) | set(exclusion))


#str_json_data = '{"id":"3","soid":"2","siid":"1","nb_soid":"3366","nb_siid":"2410","blacklist":[{"w":"bl 1","status":0}],"keywords":{"tags_s":{"w":"$EDEN,$EDENN","i":"string","e":"string","c":"string"},"tags_h":{"w":"string","i":"string","e":"string","c":"string"},"tags_a":{"w":"string","i":"string","e":"string","c":"string"},"keywords_en":{"w":"string","i":"string","e":"string","c":"string"},"keywords_de":{"w":"string","i":"string","e":"string","c":"string"}}}'
#json_data = json.loads(str_json_data)

#item = SentifiSearchItem(json_data)
#item.display()