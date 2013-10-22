from IOUtils import IOUtils
import numpy
from numpy import array
import pprint

def _build():
    file_path = "D:\\SENTIFI_DATA\\categorization\\20131021_compare_twitter_analyst.csv"
    data = IOUtils().read_list_from_csv(file_path)

    cat1_confusing_matrix(data)


def profile_type_matrix(data):
    pass

def cat1_confusing_matrix(data):
    analyst_results = data
    machine_results = data

    n = len(data)    #Number of cases

    print "Total cases:", n

    array_human = array(analyst_results)[1:,5]     #Select only column 5th from the 2nd row
    array_machine = array(machine_results)[1:,9]    #Selecting only column 9th from the 2nd row

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
    del grand_dict[0]
    print grand_dict
    dimension = len(grand_dict)
    print dimension

    confusing_matrix = numpy.zeros((dimension,dimension),dtype=numpy.int)

    #Travel each row in data
    for i in range(0, n-1):
        if (array_machine[i] != ""):
            #print array_human[i], "-------", array_machine[i]
            human_index = get_index(array_human[i], grand_dict)
            machine_index = get_index(array_machine[i], grand_dict)
            #print human_index, "---------", machine_index
            confusing_matrix[human_index][machine_index] += 1
            #print human_index, machine_index, confusing_matrix[human_index][machine_index]


    print confusing_matrix

    list_results = confusing_matrix.tolist()

    #IOUtils().save_list_to_csv(grand_dict, list_results, "D:\\matrix.csv")


    #print matches, "in total of", total_cases, "Precise =", (matches *100)/total_cases

    for item in grand_dict:
        print item


def get_index(value, dict):
    for index in range(0, len(dict)):
        if value == dict[index]:
            return index

def abc():
    #For each term in grand dictionary (confusing_matrix)
    for i in range(0, dimension-1):
        value = grand_dict[i]
        for j in range(0, n-1):

            #get index in dictionary
            index = get_index(array_human[j], grand_dict)

            # if machine got a prediction different from human's one
            if array_machine[j] == value and array_machine[j] != array_human[j]:
                confusing_matrix[i][index] += 1
            #Human and Machine match each other
            elif array_machine[j] == array_human[j]:
                confusing_matrix[index][index] += 1



_build()