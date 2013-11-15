__author__ = 'vinh.vo@sentifi.com'

import pymongo

client = pymongo.MongoClient('localhost', 27017)

db = client.twitter_publisher

print db.name

print db.carl_ikahn.find_one()


for item in db.carl_ikahn.find():
    print item['description']





