__author__ = 'nadan'

import MySQLdb
from datetime import date
from datetime import timedelta
from sys import argv
import csv


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


if __name__ == '__main__':
    current = date.today()

    if len(argv) > 1:
        current = date.strftime(argv[1], '%Y-%m-%d')

    machine_list = ['s-tag', 'tn-tag', 'followers', 'mention', 'NBIP']

    stat = {}
    analyst_name_set = set()

    with open('/home/ec2-user/PublisherReport/report/PublisherReport-' + current.isoformat() + '.csv', 'wb') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(['Machine Name', 'Total', 'Audited'])
        for machine_name in machine_list:
            statistic = twitter_publisher_statistics(machine_name, current)
            csv_writer.writerow(
                [machine_name, str(statistic['total']), str(statistic['total_audited'])])

            for name in statistic['analyst'].keys():
                if name not in analyst_name_set:
                    analyst_name_set.add(name)
                    stat[name] = {
                        'total_audited': statistic['analyst'][name].get('total_audited', 0),
                        'audited_last_7_days': statistic['analyst'][name].get('audited_last_7_days', 0),
                        'audited_yesterday': statistic['analyst'][name].get('audited_yesterday', 0)
                    }
                else:
                    stat[name]['total_audited'] += statistic['analyst'][name].get('total_audited', 0)
                    stat[name]['audited_last_7_days'] += statistic['analyst'][name].get('audited_last_7_days', 0)
                    stat[name]['audited_yesterday'] += statistic['analyst'][name].get('audited_yesterday', 0)

        csv_writer.writerow([])
        csv_writer.writerow(['Analyst Name', 'Total Audited', 'Last 7 days', 'Yesterday'])
        analyst_list = stat.keys()
        analyst_list.sort()
        for name in analyst_list:
            csv_writer.writerow([name,
                                 stat[name]['total_audited'],
                                 stat[name]['audited_last_7_days'],
                                 stat[name]['audited_yesterday']])
