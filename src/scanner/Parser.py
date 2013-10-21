import codecs
import csv
import MySQLdb

def main():
    PATH = "D:\\online-cloud\\Dropbox\\SENTIFI\\"
    FILE_PATH = PATH + "keyword.csv"

    file = codecs.open(FILE_PATH, "rb")
    reader = csv.reader(file)
    keywords = []
    for row in reader:
        #split into token by comma
        list = row[0].split(',')
        for item in list:
            #removing AND
            lst = item.split(' AND ')
            for i in lst:
                keywords.append(i.strip())
    file.close()

    print len(keywords)
    unduplicated_list = set(keywords) #remove duplication if any

    sorted_list = sorted(unduplicated_list)

    #sorted_list = sorted_list.remove(" ")
    print len(sorted_list)
    del sorted_list[0]
    print len(sorted_list)

    i = 0
    keywords = []
    word_counts = []
    values = []
    for kw in sorted_list:
        #lower
        lower_kw = kw.lower()

        #replace double quote in phrase (compound noun) by using dash between word
        skw = lower_kw.strip("'")

        #replacing space by hyphen
        hyphen_kw = skw.replace(" ", "-")

        keywords.append(hyphen_kw)
        count = hyphen_kw.count("-")
        word_counts.append(count+1)
        values.append((hyphen_kw, count+1))
        #print hyphen_kw, count+1
    pass

    #sorted_keywords = sorted(keywords)
    #word_counts

    #remove the first one

    #remove any duplication
    pure_values = set(values)
    print len(pure_values)

    #insert to database
    db = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='',db='sentifi_category')
    cursor = db.cursor()

    cursor.executemany("""INSERT INTO keywords(keyword, word_count) VALUES(%s,%s)""", pure_values)


if __name__ == '__main__':
    main()