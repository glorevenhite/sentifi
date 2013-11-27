__author__ = 'Vince'

import MySQLdb
from IOUtils import IOUtils

SERVER = 'localhost'
USERNAME = 'root'
PASSWORD = 'qscwdv'
DATABASE = 'new_community'

FILE_PATH = 'epm.csv'

#column of screen_name
SCREEN_NAME_COLUMNS = 0

#connection database
connection = MySQLdb.connect(SERVER, USERNAME, PASSWORD, DATABASE)
cursor = connection.cursor()


def get_audited_screen_name():
    sql = "SELECT twitter_screen_name FROM tbl_twitter"
    cursor.execute(sql)
    rows = cursor.fetchall()

    result = []
    for r in rows:
        result.append(r[0])

    return result


def get_categorized_screen_name():
    sql = "SELECT twitter_screen_name FROM tbl_searched_profiles_from_twitter"
    cursor.execute(sql)
    rows = cursor.fetchall()

    result = []
    for r in rows:
        result.append(r[0])

    return result


def get_uncategorized_screen_name():
    sql = "SELECT twitter_screen_name FROM tbl_uncategorized_searched_profiles_from_twitter"
    cursor.execute(sql)
    rows = cursor.fetchall()

    result = []
    for r in rows:
        result.append(r[0])

    return result


def get_checking_profiles():
    return IOUtils().read_list_from_csv(FILE_PATH)
    #return ['A', 'B', 'C', 'D', 'A']

#profiles
list_rows = get_checking_profiles()
print "START:", len(list_rows)

dict_profiles = {}
#Check duplication its self
for row in list_rows:
    screen_name = row[SCREEN_NAME_COLUMNS]
    dict_profiles[screen_name] = row

list_checking_screen_name = list(set(dict_profiles.keys()))
print "AFTER checking with itself:", len(list_checking_screen_name)

#check duplication with audited
audited_profiles_screen_name = get_audited_screen_name()
list_checking_screen_name = list(set(list_checking_screen_name) - set(audited_profiles_screen_name))
print "AFTER checking with", len(audited_profiles_screen_name), "audited profiles:", len(list_checking_screen_name)


#check duplication with categorized profiles
categorized_screen_name = get_categorized_screen_name()

list_checking_screen_name = list(set(list_checking_screen_name) - set(categorized_screen_name))
print "AFTER checking with", len(categorized_screen_name), "categorized_screen_name:", len(list_checking_screen_name)


#check duplication with categorized profiles
uncategorized_screen_name = get_uncategorized_screen_name()
list_checking_screen_name = list(set(list_checking_screen_name) - set(uncategorized_screen_name))
print "AFTER checking with", len(uncategorized_screen_name), "uncategorized_screen_name:", len(list_checking_screen_name)

#print list_checking_screen_name

list_results = []
for screen_name in list_checking_screen_name:
    list_results.append(dict_profiles[screen_name])

IOUtils().save_list_to_csv(None, list_results, "profile_results.csv")