from utils.PathUtils import PathUtils
from utils.IOUtils import IOUtils

from SentifiTwitterProfile import SentifiTwitterProfile

def main():
    PATH_TO_MENTION_FILES = "D:\\SENTIFI_DATA\\mention\\output\\"
    #TEST_PATH = "D:\\online-cloud\\Dropbox\\SENTIFI\\mention\\all\\test\\"

    profile_tags_dictionary = {}
    mention_tag = []
    twitter_id_list = []

    total_mention_count = 0    #Total mentions for all tag
    total_mention_tag = 0

    list_mention_files = PathUtils().get_list_filename(PATH_TO_MENTION_FILES)


    #for testing purpose
    #list_mention_files = get_list_filename(TEST_PATH)

    for filename in list_mention_files:
        tag = filename.replace('.csv', '')
        mention_tag.append(tag)


    for filename in list_mention_files:

        #Full file_path
        file_path = PATH_TO_MENTION_FILES + filename

        #file_path = TEST_PATH + filename

        #get profiles in file contains mention
        list_profiles = _get_profiles_from_file_path(file_path)

        #Current tag
        current_tag = filename.replace(".csv","")

        pair_tag_and_count = {current_tag:0}

        #Walking through the list of profiles
        for profile in list_profiles:
            #using twitter_id as key
            key = profile.twitter_id

            #If profile has not existed yet in dictionary. Adding profile
            if key not in profile_tags_dictionary.keys():
                #setting count of current tag is 1
                pair_tag_and_count = {current_tag:1}

                #append value to values of dictionary
                values = []
                values.append(profile)
                values.append(pair_tag_and_count)
                values.append(total_mention_count)    #counting number of mentioning
                profile_tags_dictionary.update({key:values})

                print key, values

            #profile has been existed
            else:
                values = profile_tags_dictionary.get(key)

                pair_tag_count = values[1]

                #if tag exist (same file). Increasing count of mention_tag by 1
                if pair_tag_count.get(current_tag) is not None:

                    current_count = pair_tag_and_count.get(current_tag)

                    pair_tag_and_count.update({current_tag: current_count + 1})

                    #Append
                    values.append(profile)
                    values.append(pair_tag_and_count)


                    #current_values = profile_tags_dictionary[key]    #this is a list contains two elements (profile_object, tag_and_count)
                    #current_pair_tag_and_count = current_values[1]
                    #values.append(profile)
                    #values.append(current_pair_tag_and_count)
                    #current_pair_tag_and_count.update({current_tag: 1})

                    profile_tags_dictionary.update({key:values})

                else: #tag not exist (moving to different file). #add new tag and count
                    current_values = profile_tags_dictionary[key]    #this is a list contains two elements (profile_object, tag_and_count)
                    current_pair_tag_and_count = current_values[1]
                    current_pair_tag_and_count.update({current_tag: 1})
                    values.append(profile)
                    values.append(current_pair_tag_and_count)


                profile_tags_dictionary.update({key:values})

            #print key, current_tag


        print "There are",len(list_profiles), "profiles in", filename

    print len(profile_tags_dictionary)

    _save_to_cvs_file(profile_tags_dictionary)


def _save_to_cvs_file(dictionary):
    list = []
    values = dictionary.values()

    for item in dictionary.values():
        profile = item[0]
        profile_as_list = profile.parse_to_list()

        pair_tag_count = item[1]


        #print pair_tag_count
        list_tag_count = [[k,v] for (k,v) in pair_tag_count.items()]
        tag_count = []
        for item in list_tag_count:
            tag_count += item

        #total_mention_count
        list1 = []
        total_mention_count = 0
        total_tag_count = 0
        for item in pair_tag_count.values():
            total_mention_count += item
            total_tag_count += 1
        list1.append(total_mention_count)
        list1.append(total_tag_count)

        list.append(profile_as_list + list1 + tag_count)
    header = ""
    IOUtils().save_list_to_csv(header, list, "D:\\results.csv")


def _get_profiles_from_file_path(file_path):
    profiles = []

    #Mentioning file
    list = IOUtils().read_list_from_csv(file_path)

    #remove 4 first columns
    for x in list:
        del x[0]
        del x[0]
        del x[0]
        del x[0]

    profiles_list = list

    for item in profiles_list:
        profile = SentifiTwitterProfile()

        profile.twitter_id = item[0]
        #profile.created_at = item[1]
        profile.screen_name = item[1]
        profile.full_name = item[2]
        profile.address = item[3]
        profile.email = item[4]
        profile.website_url = item[5]
        profile.website_full_url = item[6]
        profile.description = item[7]
        profile.image = item[8]
        profile.thumnail = item[9]
        profile.followers_count = item[10]
        profile.friends_count = item[11]
        profile.statuses_count = item[12]
        profile.listed_count = item[13]

        profiles.append(profile)

    return profiles

def _read_combined_profile_from_cvs(file_path):

    pass


if __name__ == "__main__":
    main()