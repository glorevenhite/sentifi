class Rule(object):
    def __init__(self):
        self.inc_keywords = []
        self.exc_keywords = []
        self.keywords = []

#===============================================================================
#    def __init__(self, inclusion_list, exclusion_list ):
#        self._inc = inclusion_list
#        self._exc = exclusion_list
#        self.keywords = self._inc + self._exc
#        self.inc_keywords = set(inclusion_list)
#        self.exc_keywords = set(exclusion_list)
#===============================================================================
    def get_inclusion(self):
        return [word.lower() for word in self.inc_keywords]

    def get_exclusion(self):
        return [word.lower() for word in self.exc_keywords]

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