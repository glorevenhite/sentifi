__author__ = 'vinh.vo@sentifi.com'

from SentifiField import SentifiField
from Constant import *
from Client import Client
from TwitterProfile import TwitterProfile
from CategorisationMatrix import CategorisationMatrix
from RuleSet import RuleSet
from Rule import Rule


class Categorizer(object):
    def categorize_twitter_profile_step(self, list_profiles):
        for profile in list_profile:

            #taking examining fields
            field_full_name = SentifiField(FIELD_TWITTER_FULL_NAME_ID, profile.fullname)
            field_screen_name = SentifiField(FIELD_TWITTER_SCREEN_NAME_ID, profile.screen_name)
            field_description = SentifiField(FIELD_TWITTER_DESCRIPTION_ID, profile.description)

            # Put above fields into a list
            fields = {TWITTER_FULL_NAME: field_full_name, TWITTER_SCREEN_NAME: field_screen_name, TWITTER_DESCRIPTION: field_description}

            # Given a P
            stage = 'Category 1'
            parent = "Financial Market Professionals"

            list_classes = self.get_classes_by_phase(stage, parent)

            #matrix = self._create_categorisation_result_matrix(fields.keys(), list_classes)
            matrix = CategorisationMatrix(fields.keys(), list_classes)

            for field in fields.values():
                field_id = field.id
                list_rule_subset = self._get_rule_subset_by_phase_field_parent(stage, field_id, parent)
                print "rule:", list_rule_subset

                if list_rule_subset is not None:
                    for subset in list_rule_subset:
                        #subset.display()
                        #print subset.cat_name
                        score = field.apply_rule_subset(subset)
                        #print score
                        matrix.increase_by(field_id, subset.cat_name, score)
                        assigned_class = matrix.get_class_name()
                        profile.set_category(stage, assigned_class)


    @staticmethod
    def _get_parent_class_name(stage, cat_name):

        message = {'type': 'parent', 'category_name': cat_name}
        print "looking for parent for:", cat_name
        client = Client()
        result = dict(client.send(message))
        print result
        return result

    @staticmethod
    def _get_rule_subset_by_phase_and_field(stage_name, field_id):
        list_rulesets = []

        message = {'type': 'subset', 'phase': stage_name, 'field_id': field_id}
        client = Client()

        # format:
        # {cat_name:
        #   {subset_id:{'exclusion':[n1,n2,n3], 'rules':{rid:[a1,b1],rid:[a2,b1]}},
        #    subset_id:{'exclusion':[m1,m2,m3], 'rules':{r
        # id:[x1,y1], rid:[x1,y2}}}
        result = dict(client.send(message))

        if result.get('status') == SERVER_STATUS_OK and result.get('data') != {}:

            dict_rule_subsets = result.get('data')
            #pprint.pprint(dict_rule_subsets)

            for cat_name in dict_rule_subsets.keys():
                subsets = dict_rule_subsets.get(cat_name)

                for subset in subsets:
                    ss = RuleSet()
                    ss.cat_name = cat_name
                    ss.exclusion = subsets.get(subset).get('exclusion')
                    rules = subsets.get(subset).get('rules').values()

                    for rule in rules:
                        r = Rule()
                        r.inc_keywords = rule
                        ss.rules.append(rule)
                    list_rulesets.append(ss)

        return list_rulesets

    @staticmethod
    def _get_rule_subset_by_phase_field_parent(stage_name, field_id, parent_id):
        list_rulesets = []

        message = {'type': 'subset', 'phase': stage_name, 'field_id': field_id, 'parent_id': parent_id}
        client = Client()

        # format:
        # {cat_name:
        #   {subset_id:{'exclusion':[n1,n2,n3], 'rules':{rid:[a1,b1],rid:[a2,b1]}},
        #    subset_id:{'exclusion':[m1,m2,m3], 'rules':{r
        # id:[x1,y1], rid:[x1,y2}}}
        result = dict(client.send(message))

        if result.get('status') == SERVER_STATUS_OK and result.get('data') != {}:

            dict_rule_subsets = result.get('data')
            #pprint.pprint(dict_rule_subsets)

            for cat_name in dict_rule_subsets.keys():
                subsets = dict_rule_subsets.get(cat_name)

                for subset in subsets:
                    ss = RuleSet()
                    ss.cat_name = cat_name
                    print subset
                    ss.exclusion = subsets.get(subset).get('exclusion')
                    rules = subsets.get(subset).get('rules').values()

                    for rule in rules:
                        r = Rule()
                        r.inc_keywords = rule
                        ss.rules.append(rule)
                    list_rulesets.append(ss)

        return list_rulesets

    def _create_categorisation_result_matrix(self, field_names, list_classes):

        matrix = CategorisationMatrix(list_field_names, list_class_names)

        return matrix

    def _create_categorisation_result_matrix2(self, field_names, phase, parent):
        #get all classes to which a profile will be assigned in given phase

        list_class_names = self._get_classes_by_phase_name(phase, parent)
        list_field_names = field_names

        matrix = CategorisationMatrix(list_field_names, list_class_names)

        return matrix

    @staticmethod
    def _get_rules_by_phase_and_field(stage_name, field_id):
        message = {'type': 'ruleset', 'phase': stage_name, 'field_id': field_id}
        client = Client()

        result = dict(client.send(message))

        return result

    @staticmethod
    def get_classes_by_phase(phase, parent_class):
        message = {'type': 'classes', 'phase': phase, 'parent_class': parent_class}
        client = Client()
        returned_data = dict(client.send(message))

        result = {}
        print "list", returned_data
        if returned_data['status'] == SERVER_STATUS_OK:
            result.update({phase: returned_data.get('data').get(phase)})

        print result.get(phase).values()
        return result.get(phase).values()


json = {'screen_name': 'glorevenhite', 'description': 'I am a financial analyst', 'name': 'Vo Truong Vinh'}
p = TwitterProfile(json)
p.screen_name = "glorevenhite"
p.description = "I am an equity analyst sell side"
p.fullname = 'Vo Truong Vinh'

list_profile = [p]

#print Categorizer().categorize_twitter_profile(list_profile)
#Categorizer()._get_classes_by_phase_name('Category 1')
Categorizer().categorize_twitter_profile_step(list_profile)