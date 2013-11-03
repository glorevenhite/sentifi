from SentifiWordsBank import  SentifiWordsBank
import simplejson


class Rule(object):
    def __init__(self, list_records):
        self.class_name = list_records[0][1]
        self.primitive_rules = list_records

    def get_regex_inclusion_str(self):
        inclusion_set = self.primitive_rules[:, 4]

        list_item = []
        for item in inclusion_set:

            if len(item.strip().split()) > 1:   # compound words
                item = '"' + item + '"'
            list_item.append(item)

        return " ".join(list_item)

    def display(self):
        #print self.class_name
        #print self.get_regex_inclusion_str()
        pass

