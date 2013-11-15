__author__ = 'vinh.vo@sentifi.com'

import pymongo

SERVER = 'localhost'
PORT = 27017


def connect_mongodb():
    return pymongo.Connection(SERVER, PORT)


def check_db_exist(dbname):
    connection = connect_mongodb()

    if str(dbname) in connection.database_names():
        return True
    return False


def drop_db(dbname):
    connection = connect_mongodb()

    if check_db_exist(dbname):
        print 'Database ', dbname, "existed. Dropping it"
        connection.drop_database(dbname)
        return True

    return False


def check_table_exist(dbname, table_name):
    if check_db_exist(dbname):
        connection = pymongo.Connection(SERVER, PORT)
        db = connection[str(dbname)]

        if str(table_name) in db.collection_names():
            return True
    return False


def create_db(dbname):
    connection = connect_mongodb()
    drop_db(dbname)
    return connection[dbname]


def create_collection(database_name, table_name):
    if drop_db(database_name):
        db = create_db(database_name)
        return db[table_name]
    return False


print check_db_exist('sport_machine')
print check_table_exist('sport_machine', 'sport_publisher')


