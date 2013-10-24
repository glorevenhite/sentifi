from pip.backwardcompat import u
from Rule import Rule


class SentifiField(object):
    def __init__(self, content):
        self.content = content

    def is_complied(self, rule):
        wordsbank = rule.get_wordsbank()

        hyphen_content = self._hyphenize_compound_words_in(wordsbank)

        tokenized_content = hyphen_content.split(" ")

        inclusion = rule.get_inclusion()
        exclusion = rule.exc_keywords

        return self._apply_filter(tokenized_content, inclusion, exclusion)

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

    def _hyphenize_compound_words_in(self, list_words):
        #strip space in left and right
        processing_content = self.content.strip()

        #replace multi-space by sing space
        processing_content = processing_content.replace("  ", " ")

        #replace hyphen in compound-word by space
        vocabulary = []
        sorted_dictionary = self._build_sorted_dictionary(list_words)
        for word in sorted_dictionary:
            #change hyphen-words into normal
            usual_word = word.replace('-', ' ')

            #put that word into new vocabulary
            vocabulary.append(usual_word)

        #Replace 'compound words' in content by the one with hyphen, i.e. compound-words
        for cw in sorted_dictionary:
            #temporaly
            tmp = cw.replace("-", " ")
            processing_content = processing_content.replace(tmp, cw)

        return processing_content

    #Dictionary sorted by number of single words
    def _build_sorted_dictionary(self, list_words):

        dict_word = {}
        for phrase in list_words:
            #spliting using space
            splitted_words = phrase.split(" ")
            words_count = len(splitted_words)

            #replacing space by hyphen then lowercase
            hyphen_phrase = phrase.replace(" ", "-").lower()
            dict_word.update({hyphen_phrase: words_count})

        sorted_dictionary = sorted(dict, key=lambda k: dict[k], reverse=True)

        return sorted_dictionary