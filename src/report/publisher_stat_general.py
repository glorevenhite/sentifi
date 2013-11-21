__author__ = 'nadan'

import MySQLdb
from datetime import date
from datetime import timedelta
from sys import argv
import csv
from SQLReport import *


def twitter_publisher_statistics(machine_name, date):
    stat = {'name': machine_name, 'analyst': {}}
    db = MySQLdb.connect('localhost', 'root', 'qscwdv', 'new_community')
    cursor = db.cursor()
    start_date = (date - timedelta(days=7)).isoformat()
    yesterday = (date - timedelta(days=1)).isoformat()

    # NET PUBLISHER
    cursor.execute(
        '''SELECT COUNT(DISTINCT p.twitter_screen_name)
            FROM 24_09_searched_profiles_from_twitter as p
            JOIN 24_09_searched_twitter_in_keyword as k
            ON p.twitter_screen_name = k.twitter_screen_name
            WHERE k.search_item LIKE '%$%'''''
    )
    total_net_publisher_by_cash_tag = cursor.fetchone()[0]

    #


    # Taking all the ANALYST
    cursor.execute(
        '''SELECT user.username
            FROM tbl_searched_profiles_from_twitter as profile, tbl_users as user
            WHERE profile.author_id = user.id
            AND user.status <> 0
            GROUP BY user.username'''
    )
    analyst_list = cursor.fetchall()
    for name_tuple in analyst_list:
        stat['analyst'][name_tuple[0]] = {}

    #Taking profiles per tags
    cursor.execute(
        '''SELECT COUNT(*)
            FROM `tbl_searched_profiles_from_twitter`
            WHERE source = ''' + "'" + machine_name + "'"
    )
    stat['total'] = cursor.fetchone()[0]

    #Count audited profiles each tag
    cursor.execute(
        '''SELECT COUNT(*)
            FROM `tbl_searched_profiles_from_twitter`
            WHERE source = ''' + "'" + machine_name + "'" + '''
            AND audited = 1'''
    )
    stat['total_audited'] = cursor.fetchone()[0]


    cursor.execute(
        '''SELECT user.username, COUNT(*)
            FROM tbl_searched_profiles_from_twitter AS profile, tbl_users AS user
            WHERE profile.author_id = user.id AND audited = 1
            AND source = ''' + "'" + machine_name + "'" + ' GROUP BY user.username'
    )
    audited_results_set = cursor.fetchall()
    for audited_result in audited_results_set:
        if audited_result[0] in stat['analyst'].keys():
            stat['analyst'][audited_result[0]]['total_audited'] = audited_result[1]

    cursor.execute(
        '''SELECT user.username, COUNT(*)
            FROM tbl_searched_profiles_from_twitter AS profile, tbl_users AS user
            WHERE profile.author_id = user.id AND audited = 1
            AND (audited_date between ''' + "'" + start_date + "'" + ' and ' + "'" + date.isoformat() + "'" + ''')
            AND source = ''' + "'" + machine_name + "'" + ' GROUP BY user.username'
    )
    audited_results_set_last_7_days = cursor.fetchall()
    for audited_result in audited_results_set_last_7_days:
        if audited_result[0] in stat['analyst'].keys():
            stat['analyst'][audited_result[0]]['audited_last_7_days'] = audited_result[1]

    cursor.execute(
        '''SELECT user.username, COUNT(*)
            FROM tbl_searched_profiles_from_twitter AS profile, tbl_users AS user
            WHERE profile.author_id = user.id AND audited = 1
            AND audited_date >= ''' + "'" + yesterday + "'" + '''
            AND source = ''' + "'" + machine_name + "'" + ' GROUP BY user.username'
    )
    audited_results_set_yesterday = cursor.fetchall()
    for audited_result in audited_results_set_yesterday:
        if audited_result[0] in stat['analyst'].keys():
            stat['analyst'][audited_result[0]]['audited_yesterday'] = audited_result[1]

    return stat


def get_s_tag_details():
    total_days = get_total_days_for_tags()
    result = ['s-tag']

    #Total Net Duplication
    total_net_duplication = get_total_publisher_net_duplication_of_cash_tag()
    result.append(total_net_duplication)

    #total categorized
    total_categorized_profiles = get_total_categorized_profiles_by_cash_tag()
    result.append(total_categorized_profiles)

    #%cat
    result.append(total_categorized_profiles/total_net_duplication)

    #audited
    audited_profiles = get_total_audited_profiles_by_cash_tag()
    result.append(audited_profiles)

    #24h raw
    result.append(0)
    result.append(get_total_profiles_by_cash_tag()/total_days)

    #24h net
    result.append(0)
    result.append(total_net_duplication/total_days)

    #24h
    result.append(0)
    result.append(total_categorized_profiles/total_days)

    return result


def get_tn_tag_details():
    total_days = get_total_days_for_tags()

    result = ['tn-tag']

    #Total Net Duplication
    net_profiles = get_total_net_profiles_by_tn_tag()
    result.append(net_profiles)

    #total categorized
    categorized_profiles = get_categorized_profiles_by_tn_tag()
    result.append(categorized_profiles)

    #%cat
    result.append(categorized_profiles/net_profiles)

    #audited
    audited_profiles = get_audited_profiles_by_tn_tag()
    result.append(audited_profiles)

    #24h raw
    result.append(0)
    result.append(0)

    #24h net
    result.append(0)
    result.append(net_profiles/total_days)

    #24h
    result.append(0)
    result.append(categorized_profiles/total_days)

    return result


def get_linkedin_details():
    result = ['Linkedin']

    #total publisher net duplication
    total_net_duplication = get_total_categorized_linkedin_profiles()
    result.append(total_net_duplication)

    #total categorized
    total_categorized = get_total_categorized_linkedin_profiles()
    result.append(total_categorized)

    #%cat
    percentage_categorized = total_categorized/total_net_duplication
    result.append(percentage_categorized)

    #audit
    audited_profiles = get_audited_linkedin_profiles()
    result.append(audited_profiles)

    #released
    released_profiles = get_released_linked_profiles()
    result.append(released_profiles)

    #raw 24h
    result.append(0)
    result.append(0)    #avg

    #net 24h
    result.append(0)
    result.append(0)    #avg

    #cat 24h
    result.append(0)
    result.append(0)    #avg

    return result


def get_nbip_details():
    results = ['NBIP', 1080, 1080, 1, 1080, 280, 0, 0, 0, 0, 0, 0]
    return results

def get_financial_experts_details():
    results = ['Financial Experts']

    #total net duplication
    net_profiles = 201141
    results.append(net_profiles)

    #total categorized
    categorized_profiles = 35087
    results.append(categorized_profiles)

    #%cat
    percentage_categorized = categorized_profiles / net_profiles
    results.append(percentage_categorized)

    #audited profiles
    audited_profiles = get_audited_profiles_by_financial_experts()
    results.append(audited_profiles)

    #released_profiles
    released_profiles = get_released_profiles_by_financial_experts()
    results.append(released_profiles)

    return results


def get_switzerland_organisation_tags_details():
    results = ['Switzerland Organsation Tags', 4761, 504, 504/4761]
    return results


def get_switzerland_organisation_phrase():
    results = ['Switzerland Organisation Phrase', 68434, 4176, 4176/68434]
    return results


def get_carl_ikahn_details():
    return ['Carl Ikahn', 94431, 13589, 13589/94431]


def get_economist_portfolio_manager_details():
    return ['Economist Portfolio Manager', 858338, 105681, 105681/858338]


def get_trader_hedgefund_details():
    return ['Trader Hedgefund', 68086, 13963, 13963/68086]


def get_20131024_nick_tweet_adder_details():
    return ['20131024 Nick Tweet Adder', 3154, 3154, 3154/3154, 3154, 3154]


if __name__ == '__main__':
    current = date.today()

    if len(argv) > 1:
        current = date.strftime(argv[1], '%Y-%m-%d')

    with open('/home/ec2-user/PublisherReport/new_report/report/PublisherReport-' + current.isoformat() + '_new.csv', 'wb') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(['Engine Name', 'Net Profiles', 'Categorized', '%cat', 'Audited', 'Released', 'raw 24h', 'avg.raw', 'net 24h', 'avg. net', 'cat 24h', 'avg.cat'])

        s_tag = get_s_tag_details()
        csv_writer.writerow(s_tag)

        tn_tag = get_tn_tag_details()
        csv_writer.writerow(tn_tag)

        linkedin = get_linkedin_details()
        csv_writer.writerow(linkedin)

        nbip = get_nbip_details()
        csv_writer.writerow(nbip)

        financial_experts = get_financial_experts_details()
        csv_writer.writerow(financial_experts)

        economist_pm = get_economist_portfolio_manager_details()
        csv_writer.writerow(economist_pm)

        trader_hedge = get_trader_hedgefund_details()
        csv_writer.writerow(trader_hedge)

        nick = get_20131024_nick_tweet_adder_details()
        csv_writer.writerow(nick)

