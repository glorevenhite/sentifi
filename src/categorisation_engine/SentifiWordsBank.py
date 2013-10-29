

class SentifiWordsBank(object):

    # Breaking down a content into word-phrases depend on a bag of words
    # 1st step: Hyphening phrase in bag of words.
    # Replacing
    def tokenize(self, content, bag_of_words):
        #rearrange words in bag in the order of number single words.
        bag_of_words = sorted(bag_of_words, key=lambda k: len(k), reverse=True)

        #Removing duplicated, leading, ending spaces in content
        procesing_content = " ".join(content.split()).lower()

        #Replace 'compound words' in given content by the one with hyphen, i.e. compound-words
        for phrase in bag_of_words:
            #hyphening phrase
            hyphening_phrase = phrase.replace(" ", "-")

            #Replacing processing
            procesing_content = procesing_content.replace(phrase, hyphening_phrase)

        tokenized_content = set(procesing_content.split(" "))

        return tokenized_content

    def build_sorted_dictionary(self, list_words):

        dict_word = {}
        for phrase in list_words:
            #spliting using space
            splitted_words = phrase.split(" ")
            words_count = len(splitted_words)

            #replacing space by hyphen then lowercase
            hyphen_phrase = phrase.replace(" ", "-").lower()
            dict_word.update({hyphen_phrase: words_count})

        sorted_dictionary = sorted(dict_word, key=lambda k: dict_word[k], reverse=True)

        return sorted_dictionary

    def hyphenize_compound_words_in(self, content, list_words):
        #strip space in left and right
        processing_content = content.strip()

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

#bag_of_words = ['financial analyst', 'financial', 'analyst']
#content = " i am a financial analyst"
#print SentifiWordsBank().tokenize(content, bag_of_words)
