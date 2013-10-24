class TwitterCriteria(object):
    def __init__(self, json_data):
        self.soid = json_data['soid']

        s_based_words = json_data['keywords'][0]['word'].split(",")
        s_inclusion = json_data['keywords'][0]['include'].split(",")
        s_exclusion = json_data['keywords'][0]['exclude'].split(",")
        s_channel = json_data['keywords'][0]['channel'].split(",")
        self.cash_tag = TwitterCriteria('$tag',s_based_words, s_inclusion, s_exclusion, s_channel)

        h_based_words = json_data['keywords'][1]['word'].split(",")
        h_inclusion = json_data['keywords'][1]['include'].split(",")
        h_exclusion = json_data['keywords'][1]['exclude'].split(",")
        h_channel = json_data['keywords'][1]['channel'].split(",")
        self.hash_tag = TwitterCriteria('#tag',h_based_words, h_inclusion, h_exclusion, h_channel)

        a_based_words = json_data['keywords'][2]['word'].split(",")
        a_inclusion = json_data['keywords'][2]['include'].split(",")
        a_exclusion = json_data['keywords'][2]['exclude'].split(",")
        a_channel = json_data['keywords'][2]['channel'].split(",")
        self.mention_tag = TwitterCriteria('@tag',a_based_words, a_inclusion, a_exclusion, a_channel)

        en_based_words = json_data['keywords'][3]['word'].split(",")
        en_inclusion = json_data['keywords'][3]['include'].split(",")
        en_exclusion = json_data['keywords'][3]['exclude'].split(",")
        en_channel = json_data['keywords'][3]['channel'].split(",")
        self.en_tag = TwitterCriteria('en',en_based_words, en_inclusion, en_exclusion, en_channel)

        de_based_words = json_data['keywords'][4]['word'].split(",")
        de_inclusion = json_data['keywords'][4]['include'].split(",")
        de_exclusion = json_data['keywords'][4]['exclude'].split(",")
        de_channel = json_data['keywords'][4]['channel'].split(",")
        self.de_tag = TwitterCriteria('de',de_based_words, de_inclusion, de_exclusion, de_channel)

        #Blacklists
        self.blacklist = json_data['blacklists']
