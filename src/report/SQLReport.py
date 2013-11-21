__author__ = 'vinh.vo@sentifi.com'
import MySQLdb
db = MySQLdb.connect('localhost', 'root', 'qscwdv', 'new_community')
cursor = db.cursor()


def get_total_days_for_tags():
    sql = '''
        SELECT count( * )
        FROM (
            SELECT date( name_source.create_time ) , count( * ) AS num_per_day
            FROM 24_09_searched_profiles_from_twitter AS name_source, 24_09_searched_twitter_in_keyword AS keyword_source
            WHERE name_source.`twitter_screen_name` = keyword_source.`twitter_screen_name`
            AND keyword_source.search_item LIKE '%$%'
            GROUP BY date( name_source.create_time )
        ) AS stat_per_day '''
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result


###############################
def get_total_profiles_by_cash_tag():
    sql = '''SELECT COUNT(p.twitter_screen_name)
        FROM 24_09_searched_profiles_from_twitter as p
        JOIN 24_09_searched_twitter_in_keyword as k
        ON p.twitter_screen_name = k.twitter_screen_name
        WHERE k.search_item LIKE "%$%"'''
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result


def get_total_publisher_net_duplication_of_cash_tag():
    sql = '''SELECT COUNT(DISTINCT p.twitter_screen_name)
        FROM 24_09_searched_profiles_from_twitter as p
        JOIN 24_09_searched_twitter_in_keyword as k
        ON p.twitter_screen_name = k.twitter_screen_name
        WHERE k.search_item LIKE "%$%"'''

    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result


def get_total_categorized_profiles_by_cash_tag():
    sql = '''SELECT COUNT( * )
        FROM  `tbl_searched_profiles_from_twitter`
        WHERE source =  's-tag'
        AND create_time < DATE_FORMAT( NOW( ), '%Y-%m-%d')'''
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result


def get_total_audited_profiles_by_cash_tag():
    sql = '''SELECT COUNT( * )
        FROM  `tbl_searched_profiles_from_twitter`
        WHERE source =  's-tag'
            AND create_time < DATE_FORMAT(NOW(), '%Y-%m-%d')
            AND audited = 1'''
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result


def get_total_released_profiles_of_cash_tag():
    sql = '''SELECT COUNT( * )
        FROM tbl_searched_profiles_from_twitter
        WHERE  `source` =  's-tag'
            AND picked_to_release_date IS NOT NULL'''
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result


def get_24h_raw_of_cash_tag():
    sql = '''SELECT COUNT(*),
                (SELECT COUNT(*) FROM 24_09_searched_twitter_in_keyword
                    WHERE twitter_screen_name = sf.twitter_screen_name
                    AND search_item LIKE  '%$%') AS appear_times,
                (SELECT GROUP_CONCAT( DISTINCT search_item )
                    FROM 24_09_searched_twitter_in_keyword
                    WHERE twitter_screen_name = sf.twitter_screen_name
                    AND search_item LIKE  '%$%') AS Search_strings
            FROM 24_09_searched_profiles_from_twitter sf
            WHERE datediff(d,date(create_time),DATE_FORMAT(NOW(), '%Y-%m-%d'))
            GROUP BY twitter_screen_name
            HAVING appear_times >0;'''
    cursor.execute(sql)
    result = cursor.fetchall()
    return len(result)


##################################################################################################################
def get_total_net_profiles_by_tn_tag():
    sql = '''SELECT COUNT(DISTINCT p.twitter_screen_name)
        FROM 24_09_searched_profiles_from_twitter as p
        JOIN 24_09_searched_twitter_in_keyword as k
        ON p.twitter_screen_name = k.twitter_screen_name
        WHERE k.search_item LIKE "%@%" OR k.search_item LIKE "%#%"'''
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result


def get_categorized_profiles_by_tn_tag():
    sql = '''SELECT COUNT( * )
        FROM  `tbl_searched_profiles_from_twitter`
        WHERE source =  'tn-tag'
        AND create_time < DATE_FORMAT( NOW( ), '%Y-%m-%d')'''
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result


def get_audited_profiles_by_tn_tag():
    sql = '''SELECT COUNT( * )
        FROM  `tbl_searched_profiles_from_twitter`
        WHERE source =  'tn-tag'
            AND create_time < DATE_FORMAT(NOW(), '%Y-%m-%d')
            AND audited = 1'''
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result


def get_released_profiles_by_tn_tag():
    sql = '''SELECT COUNT( * )
        FROM tbl_searched_profiles_from_twitter
        WHERE  `source` =  'tn-tag'
            AND picked_to_release_date IS NOT NULL'''
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result

####################################################################################################################
#LINKEDIN
def get_total_net_linkedin_profiles():
    sql = '''SELECT (SELECT COUNT(*) FROM tbl_linkedin) + (SELECT COUNT(*) FROM tbl_linkedin_profiles_from_html);'''
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result


def get_total_categorized_linkedin_profiles():
    sql = '''SELECT (
                SELECT COUNT(*) FROM tbl_linkedin) + (
                SELECT COUNT(*) FROM tbl_linkedin_profiles_from_html
                    WHERE category_id <> -1);'''

    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result


def get_audited_linkedin_profiles():
    sql = '''SELECT (
                SELECT COUNT(*) FROM tbl_linkedin) + (
                SELECT count(*) from tbl_linkedin_profiles_from_html where audited=1);'''

    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result


def get_released_linked_profiles():
    sql = '''SELECT (SELECT COUNT(*) FROM tbl_linkedin);'''

    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result


#####################################
#EXPERTS
def get_audited_profiles_by_financial_experts():
    sql = '''SELECT count(*) from tbl_searched_profiles_from_twitter
        WHERE `source`= 'mention'
        AND document_audited in ('2013.10.18_list_of_people_talk_about_financial_experts_with_more_than_50followers.xlsx', '2013.10.21_twitter.mentioning.financial.experts_with_more_than_50followers.csv')
        AND audited= 1;'''
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result


def get_released_profiles_by_financial_experts():
    sql = '''SELECT count(*) FROM tbl_searched_profiles_from_twitter
        WHERE `source`= 'mention' AND document_audited IN (
            '2013.10.18_list_of_people_talk_about_financial_experts_with_more_than_50followers.xlsx',
            '2013.10.21_twitter.mentioning.financial.experts_with_more_than_50followers.csv')
        AND picked_to_release_date IS NOT NULL;'''
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    return result



















































































































































































































































































































































































































































































#print get_24h_raw_of_cash_tag()





