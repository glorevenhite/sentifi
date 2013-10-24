class Rule(object):
    def __init__(self, json_data):
        self.rule_set_name = json_data['rule_set_name']
        self.inc_keywords = json_data['keywords']['include'].split(",")
        self.exc_keywords = json_data['keywords']['exclude'].split(",")
        self.keywords = []

    def get_inclusion(self):
        #lowercase and strip any space in both left and right side
        return [word.lower().strip() for word in self.inc_keywords]

    def get_exclusion(self):
        #lowercase and strip any space in both left and right side
        return [word.lower().strip() for word in self.exc_keywords]

    def get_wordsbank(self):
        wordsbank = self.inc_keywords + self.exc_keywords
        return self._build_wordsbank(wordsbank)

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


    def display(self):
        print "Inclusion:"
        for kw in self.inc_keywords:
            print kw
        print "Exclusion:"
        for kw in self.exc_keywords:
            print kw
        print '-----------------'






"""For testing only"""
#rule = Rule(['financial', 'analyst'], ['trader'])
#print rule.keywords