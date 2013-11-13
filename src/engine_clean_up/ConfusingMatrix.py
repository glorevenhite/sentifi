from IOUtils import IOUtils
import numpy
from numpy import array
import pprint
from MySQLUtils import MySQLUtils

def _build():
    file_path = "D:\\Dropbox\\Sentifi Analytics\\5. Vinh\\Confusing Matrix\\2013.11.09\\results.csv"
    data = IOUtils().read_list_from_csv(file_path)

    cat1_confusing_matrix(data)


def profile_type_matrix():
    connection = MySQLUtils().connection
    cursor = connection.cursor()

    table = '20131109_copy'
    new = 'new_machine'
    old = 'old_machine_audited'

    # COMPILE for the NEW ONE
    query = "SELECT a.profile_id, a.twitter_screen_name, a.twitter_full_name, a.twitter_description, "
    query += " a.profile_type_analyst, a.Group_analyst, a.cat1_analyst, a.cat2_analyst, "
    query += " n.profile_type, n.publisher_group, n.cat1, n.cat2 "
    query += " FROM {0} AS a " .format(table)
    query += " RIGHT JOIN {0} AS n ON n.twitter_screen_name = a.twitter_screen_name " .format(new)


    #COMPARE OLD one
    #query = "SELECT a.profile_id, a.twitter_screen_name, a.twitter_full_name, a.twitter_description, "
    #query += " a.profile_type_analyst, a.Group_analyst, a.cat1_analyst, a.cat2_analyst, "
    #query += " o.profile_type_machine, o.Group_machine, o.cat1_machine, o.cat2_machine "
    #query += " FROM {0} AS a " .format(table)
    #query += " JOIN {0} AS o ON a.twitter_screen_name = o.twitter_screen_name " .format(old)

    print query

    cursor.execute(query)

    rows = cursor.fetchall()
    connection.close()

    print "a"
    cat1_confusing_matrix(rows)
    print "b"


def cat1_confusing_matrix(data):
    print "printout confusing matrix"
    analyst_results = data
    machine_results = data

    n = len(data)    #Number of cases

    print "Total cases:", n

    array_human = numpy.array(analyst_results)[0:, 6]     #Select only column 5th from the 2nd row
    array_machine = numpy.array(machine_results)[0:, 10]    #Selecting only column 9th from the 2nd row

    print 'human rows:', len(array_human)
    print 'machine_rows:', len(array_machine)


    dict = {}
    for index in range(0, n-1):
        if array_human[index] == array_machine[index]:
            keys = dict.keys()
            if array_human[index] not in keys:    #found new term
                dict.update({array_human[index]:1})
            else: #increasing count by 1
                current_count = dict[array_human[index]]
                dict.update({array_human[index]:current_count+1})

    total_matches = 0
    for count in dict.values():
        total_matches += count
    print "Total matches:", total_matches

    print len(set(array_human)), len(set(array_machine))

    ##############################################################################################3
    #Building confusing matrix
    lst1 = list(array_human)
    lst2 = list(array_machine)

    grand_dict = sorted(set(lst1 + lst2))    #Since human using much more vocabulary than machine
    del grand_dict[0]   # why delete the first one
    print grand_dict
    dimension = len(grand_dict)
    print dimension

    confusing_matrix = numpy.zeros((dimension, dimension), dtype=numpy.int)

    #Travel each row in data

    for i in range(0, n-1):
        if array_machine[i] is not None:
            print data[i][1], data[i]
            print array_human[i], "-------", array_machine[i]
            human_index = get_index(array_human[i], grand_dict)
            machine_index = get_index(array_machine[i], grand_dict)
            print array_machine[i]
            print human_index, "---------", machine_index
            confusing_matrix[human_index][machine_index] += 1
            #print human_index, machine_index, confusing_matrix[human_index][machine_index]

    print confusing_matrix

    list_results = confusing_matrix.tolist()

    IOUtils().save_list_to_csv(grand_dict, list_results, "D:\\matrix.csv")


    #print matches, "in total of", total_cases, "Precise =", (matches *100)/total_cases

    for item in grand_dict:
        print item


def get_index(value, dict):
    for index in range(0, len(dict)):
        if value == dict[index]:
            return index




profile_type_matrix()