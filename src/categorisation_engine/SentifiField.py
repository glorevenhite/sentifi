from Rule import Rule
from SentifiWordsBank import SentifiWordsBank


class SentifiField(object):
    def __init__(self, content):
        self.content = content

    def is_complied(self, rule):
        #get all words used in rule
        wordsbank = rule.get_wordsbank()

        #hyphenize any compound words in content
        hyphen_content = SentifiWordsBank().hyphenize_compound_words_in(wordsbank)

        #Splitting the hyphen_content using space resulting to a list of words used in content
        tokenized_content = hyphen_content.split(" ")

        #get words using in case of inclusion and exclusion
        inclusion = rule.get_inclusion()
        exclusion = rule.exc_keywords

        #Check whether the content has word in inclusion set but not exclusion set
        flag = self._apply_rule(tokenized_content, inclusion, exclusion)

        return flag

    def _apply_rule(self, tokenized_content, inclusion, exclusion):

        #Check whether content contains any word in exclusion set
        exc = set(tokenized_content.split(" ")) & set(exclusion)
        if len(exc) > 0:    # contains word in exclusion set
            return False

        innersection = set(tokenized_content.split(" ")) & set(inclusion)

        if len(innersection) == len(set(inclusion)):
            return True
        else:
            return False