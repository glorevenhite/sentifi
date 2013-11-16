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

    cursor.execute(
        '''SELECT COUNT(*)
            FROM `tbl_searched_profiles_from_twitter`
            WHERE source = ''' + "'" + machine_name + "'"
    )
    stat['total'] = cursor.fetchone()[0]

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

    with open('/home/ec2-user/PublisherReport/report/PublisherReport-' + current.isoformat() + '.csv', 'wb') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        for machine_name in machine_list:
            statistic = twitter_publisher_statistics(machine_name, current)
            csv_writer.writerow([machine_name,
                                 'Total',
                                 str(statistic['total']),
                                 'Audited',
                                 str(statistic['total_audited'])])
            csv_writer.writerow(['Analyst Name',
                                 'Total Audited',
                                 'Last 7 days',
                                 'Yesterday'])
            analyst_list = statistic['analyst'].keys()
            analyst_list.sort()
            for name in analyst_list:
                csv_writer.writerow([name,
                                     str(statistic['analyst'][name].get('total_audited', 0)),
                                     str(statistic['analyst'][name].get('audited_last_7_days', 0)),
                                     str(statistic['analyst'][name].get('audited_yesterday', 0))])
            csv_writer.writerow([])
