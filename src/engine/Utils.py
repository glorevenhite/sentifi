__author__ = 'vinh.vo@sentifi.com'


def look(list_keywords, content):
    list_token_content = content.split()
    if (set(list_keywords) & set(list_token_content)) == set(list_keywords):
        return True

def get_keywords_from_nth_box():
    pass


def get_inclusion():
    pass



if __name__ == "__main__":
    pass
    #list_keywords = ['financial', 'analyst']
    #content = "I am a financial analyst"
    #print look(list_keywords, content)


