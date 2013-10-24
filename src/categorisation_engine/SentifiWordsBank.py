import MySQLdb
import pprint
from Rule import Rule


class SentifiWordsBank(object):

    def tokenizer(self, content, keywords):

        #strip space in left and right
        content = content.strip()

        #replace multi-space by sing space
        content = content.replace("  ", " ")

        #replace hyphen in compound-word by space
        vocabulary = []
        for v in keywords:
            vocabulary.append(v.replace('-', ' '))

        #Replace 'compound words' in content by the one with hyphen, i.e. compound-words
        for cw in keywords:
            #temporaly
            tmp = cw.replace("-", " ")
            content = content.replace(tmp, cw)
        return content

    def build_sorted_dictionary(self, list_words):

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

    def hyphenize_compound_words_in(self, list_words):
        #strip space in left and right
        processing_content = self.content.strip()

        #replace multi-space by sing space
        processing_content = processing_content.replace("  ", " ")

        #replace hyphen in compound-word by space
        vocabulary = []
        sorted_dictionary = SentifiWordsBank().build_sorted_dictionary(list_words)
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

    def get_compound_word(self):
        compound_nount = []

        self._cursor.execute("SELECT keyword FROM keywords WHERE word_count > 1 ORDER BY word_count DESC")
        compound_noun = self._cursor.fetchall()

        return compound_noun
        pass

#print(SentifiWordsBank().wordsbank)
#print(SentifiWordsBank().get_compound_word())
#print len(SentifiWordsBank().wordsbank)
#content = "name of any listed financial newsprovider firm of consulting trading company financial system analyst forex trader"
#print SentifiWordsBank().tokenizer(content)
