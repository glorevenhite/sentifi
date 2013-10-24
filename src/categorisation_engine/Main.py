import MySQLdb
from text.blob import TextBlob
import nltk
import pprint


from Classifier import Classifier
from Ruler import Ruler
from Constant import *
from TwitterProfile import TwitterProfile

def main():
    """ INPUT: file_path_to_profiles_cvs. Each line is a profile
        OUTPUT: file with content in format: fullname, desc, profile_type, publisher_group, cat_1, cat_2
    """

    #

    #rs1 = Ruler().load_all_ruleset(Category().PER)
    #rs2 = Ruler().load_all_ruleset(Category().ORG)
    #rs3 = Ruler().load_all_ruleset(Category().NEWS)

    #rules = []
    #rules.append(rs1)
    #rules.append(rs2)
    #rules.append(rs3)

    profiles = []

    #Profile 1

    n1 = 'glorevenhite'
    d1 = 'i am a student who want to become a financial analyst'
    p1 = TwitterProfile(n1,d1)


    #Profile 2
    n2 = 'finc'
    d2 = 'we provide good services in financial advisory'
    p2 = TwitterProfile(n2, d2)

    profiles.append(p1)
    profiles.append(p2)

    pfs = Classifier().classify_twitter_profile(profiles)


    for p in pfs:
       p.display()

    #a = Classifier().classify_profile_type('hello i am', rules)
    #print a

    #wiki = TextBlob("Python is a high-level, general-purpose programming language financial-analyst.")
    #print wiki.words

    """
    db = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='',db='sentifi_category')
    cursor = db.cursor()

    cursor.execute('SELECT category_name FROM tbl_categories')

    result = cursor.fetchall()
    for row in result:
        #pprint.pprint(row)
        print row

        """

if __name__ == "__main__":
    main()



