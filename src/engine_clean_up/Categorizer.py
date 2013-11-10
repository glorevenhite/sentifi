from MySQLUtils import MySQLUtils
from SentifiTwitterProfile import SentifiTwitterProfile
from JSonFeeder import JSonFeeder
from Utils import *
from Constant import *
import shelve
import numpy


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

        #Extract rules
        #list_rules = sentifi_category.get_rules()
        #for rules in list_rules:
        #    if isinstance(rules, tuple):  # tuple
        #        if match_and(rules, content):
        #            score += len(rules)
        #    elif type(rules) == type(u''):
        #        list_keywords = [rules]
        #        if match_and(list_keywords, content):
        #            score += len(rules.split())

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

                #s = match_or(query.based_words, content)
                #if s > 0:        # contains word in FIRST BOX
                #    tmp_score += s
                #
                #    s = match_or(query.and1_words, content)
                #    if s > 0:     # contains word in FIRST AND BOX
                #        tmp_score *= s
                #
                #        s = match_or(query.and2_words, content)
                #        if len(query.and2_words) and s > 0:     # contains word in SECOND BOX
                #            tmp_score *= s
                #        else:
                #            tmp_score = 0   # do not match continuously second AND box
                #    elif len(query.and1_words) == 0 and s == 0:  # score = 0 since no there is no keywords
                #        tmp_score = 0
            score += tmp_score
        return score

if __name__ == "__main__":
    f = open('log.txt', 'a')

    try:
        database = shelve.open(PATH_CACHE)
        list_sentifi_categories = database['sc']
        json_category_names = database['cn']
        database.close()

        profile = SentifiTwitterProfile([1, 'marcbrse invest', 'glorevenhite', 'marcrse invest & market solutions'])
        Categorizer().categorizer(profile, list_sentifi_categories, json_category_names )
        profile.display()

        connection = MySQLUtils().connection
        cursor = connection.cursor()
        sql = "SELECT * FROM {0} " .format(TABLE_PROFILES_INPUT)
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            p = SentifiTwitterProfile(row)
            print p.screen_name
            Categorizer().categorizer(p, list_sentifi_categories, json_category_names)
            #p.display()
            arr_values = p.to_array()

            string = ['%s']*len(arr_values)

            #Joining list of %s by comma
            var_st = ','.join(string)

            #Building query string
            query_str = 'INSERT INTO ' + TABLE_PROFILES_OUTPUT + ' VALUES(%s)' % var_st

            #Execute query and commit
            cursor.execute(query_str, arr_values)

            connection.commit()
    except Exception, e:
        f.write(str(e) + '\n')





