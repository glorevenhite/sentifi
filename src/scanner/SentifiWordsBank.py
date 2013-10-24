import MySQLdb
import pprint
from Rule import Rule
class SentifiWordsBank(object):
    def __init__(self):
        pass
    @property
    def wordsbank(self):
        return self._wordsbank

    @wordsbank.setter
    def wordsbank(self, value):
        self._wordsbank = value

    def add_word(self, word):
        self._wordsbank.append(word)

    def get_compound_words(self):
        pass

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

    def build_keywords(self, ruleset):
        keywords = []
        # Having ruleset must be applied to field. Some field_content don't have any rule to dectect PROFILE_TYPE, exp: fullname of Personal
        if (ruleset != None):
            for r in ruleset:
                keywords = keywords + r.keywords
        return keywords

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
