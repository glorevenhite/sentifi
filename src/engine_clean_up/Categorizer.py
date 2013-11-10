from MySQLUtils import MySQLUtils
from SentifiTwitterProfile import SentifiTwitterProfile
from JSonFeeder import JSonFeeder
from Utils import *
from Constant import *
import sys
import shelve
import numpy
import thread
import time


class Categorizer(object):

    def categorizer(self, profile, list_sentifi_categories, json_category_names):

        #Take the fields need to be scan
        fields = profile.get_fields()
        field_description = fields[2]
        field_full_name = fields[1]

        #Identify whether a profile is Person or Organisation
        pid = None
        candidates = []
        candidates.extend(JSonFeeder.get_sentifi_category_by_field(pid, TWITTER_DESCRIPTION, list_sentifi_categories))
        assigned_category = self.assign(field_description, candidates)

        if assigned_category is not None:   #Knowing ITEM FILE
            profile.profile_type = assigned_category

            # We now know the type of given profile. Just keep allocate profile in a straight way.
            # However, we'll go to the stage of identifying CAT1 instead of identifying ITEM GROUP

            if profile.profile_type == PERSONAL:
                pids = [4, 5]
            else:
                pids = [6, 7, 8, 9, 10, 11, 12, 13]

            candidates = []
            for pid in pids:
                sc = JSonFeeder.get_sentifi_category_by_field(pid, TWITTER_DESCRIPTION, list_sentifi_categories)
                candidates.extend(sc)

            assigned_category = self.assign(field_description, candidates)

            if assigned_category is not None:   # knowing CAT1
                profile.category1 = assigned_category

                #Having known CAT1, ITEM GROUP is identified as well
                profile.profile_group = JSonFeeder().get_parent_name(profile.category1, json_category_names)

                #Go to the stage of identifying CAT2
                pid = JSonFeeder.get_category_id_by_name(profile.category1, json_category_names)
                sc = JSonFeeder.get_sentifi_category_by_field(pid, TWITTER_DESCRIPTION, list_sentifi_categories)
                candidates = []
                candidates.extend(sc)

                assigned_category = self.assign(field_description, candidates)
                if assigned_category is not None:
                    profile.category2 = assigned_category
                    return
            else:   # Still cannot identify CAT1, go to stage of CAT2 and hopefully
                #Go to the stage of identifying CAT2
                pids = [45, 46, 47, 179, 52, 61, 64, 89, 68, 87, 93]
                for pid in pids:
                    sc = JSonFeeder.get_sentifi_category_by_field(pid, TWITTER_DESCRIPTION, list_sentifi_categories)
                candidates = []
                candidates.extend(sc)

                assigned_category = self.assign(field_description, candidates)
                if assigned_category is not None:   # Luckily find out CAT2
                    profile.category2 = assigned_category

                    profile.category1 = JSonFeeder().get_parent_name(profile.category2, json_category_names)
                    profile.profile_group = JSonFeeder().get_parent_name(profile.category1, json_category_names)
                    return
        else:   # Cannot detect whether profile is Person or Organisation. Going to stage of CAT1 detection
            pids = CAT1_PARENT
            candidates = []

            #For each pid, making a list of candidate categories to which profile is assigned
            for pid in pids:
                sc = JSonFeeder.get_sentifi_category_by_field(pid, TWITTER_DESCRIPTION, list_sentifi_categories)
                candidates.extend(sc)

            assigned_category = self.assign(field_description, candidates)

            if assigned_category is not None:
                profile.category1 = assigned_category
                profile.profile_group = JSonFeeder().get_parent_name(profile.category1, json_category_names)
                profile.profile_type = JSonFeeder().get_parent_name(profile.profile_group, json_category_names)

                #############################################################
                parent = profile.category1
                pid = JSonFeeder().get_category_id_by_name(parent, json_category_names)
                candidates = []
                candidates.extend(JSonFeeder().get_sentifi_category_by_field(pid, TWITTER_DESCRIPTION, list_sentifi_categories))

                if len(candidates):
                    profile.category2 = self.assign(field_description, candidates)
                else:
                    profile.category2 = None
            else:
                pids = [45, 46, 47, 179, 52, 61, 64, 89, 68, 87, 93]
                candidates = []
                for pid in pids:
                    candidates.extend(JSonFeeder().get_sentifi_category_by_field(pid, TWITTER_DESCRIPTION, list_sentifi_categories))

                if len(candidates):
                    profile.category2 = self.assign(field_description, candidates)
                    profile.category1 = JSonFeeder().get_parent_name(profile.category2, json_category_names)
                    profile.profile_group = JSonFeeder().get_parent_name(profile.category1, json_category_names)
                    profile.profile_type = JSonFeeder().get_parent_name(profile.profile_group, json_category_names)
                else:
                    profile.category2 = None


    def assign(self, field, candidate_list):
        value = None
        if len(candidate_list):
            score_board = self.check_field_against_categories(field, candidate_list)
            references = [cat.name for cat in candidate_list]
            value = get_candidate_name(score_board, references)
        return value

    # Checking whether fields satisfy
    def check_fields_against_categories(self, sentifi_fields, sentifi_categories):
        list_result = []

        # the input contains rules for all fields, so we need extract specific rules given field
        list_categories = self.get_categories(sentifi_categories)

        # For each field we will check it against a list of categories to know to which it can be classified
        # The result is an array of score indicates how good (how many time) a field contains keywords given
        for f in sentifi_fields:
            dict_results = self.check_field_against_categories(f, list_categories)
            list_result.append(dict_results)

        return list_result

    def check_field_against_categories(self, sentifi_field, sentifi_categories):
        list_results = []
        #list_category_names = [cat.name for cat in sentifi_categories]

        for cat in sentifi_categories:
            score = self.check(sentifi_field, cat)
            list_results.append(score)

        return list_results

    @staticmethod
    def get_categories(list_sentifi_categories, field):
        list_results = []

        for cat in list_sentifi_categories:
            queries = cat.queries
            for query in queries:
                if query.field == field:
                    list_results.append(cat)

        return list_results

    @staticmethod
    def check(sentifi_field, sentifi_category):
        score = 0
        #Extract only content
        content = unicode(sentifi_field.content).encode('utf-8')

        #Extract exclusion
        exclusion = sentifi_category.get_exclusion()

        if len(exclusion):
            if match_not(exclusion, content):
                score = 0
                return score

        queries = sentifi_category.queries
        tmp_score = 0
        for query in queries:
            if match_or(query.not_words, content):  # contains words in the NOT BOX
                return score
            else:
                scores = []
                if len(query.based_words) > 0:
                    s = match_or(query.based_words, content)
                    scores.append(s)
                if len(query.and1_words) > 0:
                    scores.append(match_or(query.and1_words, content))
                if len(query.and2_words) > 0:
                    scores.append(match_or(query.and2_words, content))
                arr_scores = numpy.array(scores)
                tmp_score = arr_scores.prod()

            score += tmp_score
        return score


def categorize(table_output, list_profiles, list_sentifi_categories, json_category_names):

    print "Starting categorisastion progress and input to " + table_output

    # create output database
    connection_thread = MySQLUtils().connection
    cursor_thread = connection_thread.cursor()

    sql_create_table = "CREATE TABLE {0} AS (SELECT * FROM {1}) " .format(table_output, TABLE_OUTPUT_TEMPLATE)
    cursor_thread.execute(sql_create_table)
    connection_thread.commit()

    for row in list_profiles:
        p = SentifiTwitterProfile(row)
        print p.screen_name
        Categorizer().categorizer(p, list_sentifi_categories, json_category_names)
        #p.display()
        arr_values = p.to_array()

        string = ['%s']*len(arr_values)

        #Joining list of %s by comma
        var_st = ','.join(string)

        #Building query string
        query_str = 'INSERT INTO ' + table_output + ' VALUES(%s)' % var_st

        #Execute query and commit
        cursor_thread.execute(query_str, arr_values)

        connection_thread.commit()
    connection_thread.close()


if __name__ == "__main__":
    input_table = ""
    log_file = ""
    profile_per_thread = 0

    if len(sys.argv) == 4:
        #Input table
        input_table = sys.argv[1]
        log_file = sys.argv[2]
        profile_per_thread = int(sys.argv[3])
    else:
        print "Please specify INPUT_TABLE, LOG FILE"
        exit()

    f = open(log_file, 'a')
    try:
        database = shelve.open(PATH_CACHE)
        list_sentifi_categories = database['sc']
        json_category_names = database['cn']
        database.close()

        #profile = SentifiTwitterProfile([1, 'marcbrse invest', 'glorevenhite', 'marcrse invest & market solutions'])
        #Categorizer().categorizer(profile, list_sentifi_categories, json_category_names )
        #profile.display()

        connection = MySQLUtils().connection
        cursor = connection.cursor()

        sql = "SELECT * FROM {0} " .format(input_table)
        cursor.execute(sql)
        rows = cursor.fetchall()
        connection.close()

        list_chunks = split_into_chunks(rows, profile_per_thread)
        ith = 1
        for chunk in list_chunks:
            print "Start thread..."
            output_table = input_table + TABLE_OUTPUT_TEMPLATE + str(ith)
            ith += 1
            try:
                thread.start_new(categorize, (output_table, chunk, list_sentifi_categories, json_category_names))
            except Exception, e:
                print e

            time.sleep(3)

        while 1:
            pass

    except Exception, e:
        f.write(str(e) + '\n')