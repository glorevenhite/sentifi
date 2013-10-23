from Rule import Rule
import json

class SentifiMessage(object):
    def __init__(self, text, channel, publisher):
        self.text = text
        self.channel = channel
        self.publisher = publisher
        self.status = False

    def display(self):
        print self.text, self.publisher, self.channel, self.status

class SentifiSearchItem(object):
    def __init__(self, json_data):
        s_based_words = json_data['keywords']['tags_s']['w'].split(",")
        s_inclusion = json_data['keywords']['tags_s']['i'].split(",")
        s_exclusion = json_data['keywords']['tags_s']['e'].split(",")
        self.cash_tag = SentifiSearchItemTagElement('$',s_based_words, s_inclusion, s_exclusion)

        h_based_words = json_data['keywords']['tags_h']['w'].split(",")
        h_inclusion = json_data['keywords']['tags_h']['i'].split(",")
        h_exclusion = json_data['keywords']['tags_h']['e'].split(",")
        self.hash_tag = SentifiSearchItemTagElement('#',h_based_words, h_inclusion, h_exclusion)

        a_based_words = json_data['keywords']['tags_a']['w'].split(",")
        a_inclusion = json_data['keywords']['tags_a']['i'].split(",")
        a_exclusion = json_data['keywords']['tags_a']['e'].split(",")
        self.mention_tag = SentifiSearchItemTagElement('@',a_based_words, a_inclusion, a_exclusion)

        en_based_words = json_data['keywords']['keywords_en']['w'].split(",")
        en_inclusion = json_data['keywords']['keywords_en']['i'].split(",")
        en_exclusion = json_data['keywords']['keywords_en']['e'].split(",")
        self.en_tag = SentifiSearchItemTagElement('en',en_based_words, en_inclusion, en_exclusion)

        de_based_words = json_data['keywords']['keywords_de']['w'].split(",")
        de_inclusion = json_data['keywords']['keywords_de']['i'].split(",")
        de_exclusion = json_data['keywords']['keywords_de']['e'].split(",")
        self.de_tag = SentifiSearchItemTagElement('de',de_based_words, de_inclusion, de_exclusion)

        #self.blacklist = json_data['blacklist'].split(",")
        #self.blacklist_status = json_data['blacklist'].split(",")

    def display(self):
        print self.based_words
        print self.inclusion
        print self.exclusion

class SentifiSearchItemTagElement(object):
    def __init__(self, name, based_words, inclusion, exclusion):
        self.name = name
        self.based_words = based_words
        self.inclusion = inclusion
        self.exclusion = exclusion
        self.wordsbank = list(set(based_words) | set(inclusion) | set(exclusion))
        self.ruleset = self._get_ruleset(based_words, inclusion, exclusion)

    def _get_ruleset(self, based_words, inclusion, exclusion):
        ruleset = []

        pair_inclusion = []
        for bw in based_words:
            for ic in inclusion:
                pair = [bw, ic]
                pair_inclusion.append(pair)

        #Combine each pair in inclusion_list with exclusion_list
        for pair in pair_inclusion:
            for ew in exclusion:
                rule = Rule()
                rule.inc_keywords = pair_inclusion
                rule.exc_keywords = ew
                rule_set.append(rule)

        return ruleset







        pass



class SentifiFilter(object):
    def __init__(self, based_words, inclusion, exclusion):
        self.based_words = based_words
        self.inclusion = inclusion
        self.exclusion = exclusion
        self.wordsbank = list(set(based_words) | set(inclusion) | set(exclusion))


    def get_ruleset(self):
        ruleset = []



        pass

str_json_data = '{"id":"3","soid":"2","siid":"1","nb_soid":"3366","nb_siid":"2410","blacklist":[{"w":"bl 1","status":0}],"keywords":{"tags_s":{"w":"$EDEN,$EDENN","i":"string","e":"string","c":"string"},"tags_h":{"w":"string","i":"string","e":"string","c":"string"},"tags_a":{"w":"string","i":"string","e":"string","c":"string"},"keywords_en":{"w":"string","i":"string","e":"string","c":"string"},"keywords_de":{"w":"string","i":"string","e":"string","c":"string"}}}'
json_data = json.loads(str_json_data)

item = SentifiSearchItem(json_data)
item.display()