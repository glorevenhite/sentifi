from Filter import Filter
from IOUtils import IOUtils
from SentifiMessage import SentifiMessage
from SentifiMessage import SentifiFilter
from SentifiMessage import SentifiSearchItem

import sys
import json


def main():
    HOME_PATH = "D:\\SENTIFI_DATA\\filter\\"

    FILE_PATH_TO_JSON_MESSAGES = HOME_PATH + "messages.json"
    FILE_PATH_TO_JSON_CRITERIA = HOME_PATH + "criteria.json"

    json_messages = IOUtils().read_json_data_from_file(FILE_PATH_TO_JSON_MESSAGES)
    json_criteria = IOUtils().read_json_data_from_file(FILE_PATH_TO_JSON_CRITERIA)

    list_criteria = []
    for criteria in json_criteria:
        item = SentifiSearchItem(criteria)
        list_criteria.append(item)

    list_messages = []
    for json_item in json_messages:
        message = SentifiMessage(json_item)
        list_messages.append(message)

    #For each message, compare its soid to criteria's soid
    for message in list_messages:
        for criteria in list_criteria:
            if message.soid == criteria.soid:
                filter = Filter(message, criteria)
                filter.apply()

    results = []
    for msg in list_messages:
        results.append(msg.get_json())
        results.append(msg.get_json())

    print results
    return results

if __name__ == "__main__":
    main()



