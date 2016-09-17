#coding=utf-8
import csv
import json
def proprecess(jsonfile):
    file = open(jsonfile,'r')
    count = 0

    with open('../../dataset/aiv_all.csv','a') as wf:
        writer = csv.writer(wf)
        writer.writerow(['reviewerID','asin','reviewText','overall'])
        for line in file:
            count += 1
            l = []
            js = json.loads(line)
            # if count > 5:
            #     break
            # print line
            l.append(js['reviewerID'])
            l.append(js['asin'])
            l.append(js['reviewText'])
            l.append(js['overall'])
            writer.writerow(l)


def readcsv(filename):
    with open(filename,'r') as f:
        dict_reader = csv.DictReader(f)
        count = 0
        for row in dict_reader:
            count += 1
            if count > 100:
                break
            # print(row['reviewerID'])
            # print(row['overall'])
            print(row['asin'])
            print(row['reviewText'])

def simpleCount(filename):
    with open('../../dataset/aiv.csv','r') as f:
        dict_reader = csv.DictReader(f)
        dict_reviewers={}
        dict_reviews={}
        for row in dict_reader:
            if row['reviewerID'] not in dict_reviewers:
                dict_reviewers[row['reviewerID']] = 1
            else:
                dict_reviewers[row['reviewerID']] += 1

            if row['asin'] not in dict_reviews:
                dict_reviews[row['asin']] = 1
            else:
                dict_reviews[row['asin']] += 1

        print('reviewers: ',dict_reviewers.__len__())
        print('asins: ',dict_reviews.__len__())


def removeStopWords(csvfilw):
    f = open(csvfilw,'r')
    dict_reader = csv.DictReader(f)
    count = 0
    with open('../../dataset/aiv_all_removed_stop_words.csv','a') as wf:
        asin_dict={}
        for row in dict_reader:
            count += 1
            # if count > 10:
            #     break
            doc = removePunctuation(row['reviewText'])
            # print doc
            asin_dict[row['asin']] = asin_dict.get(row['asin'],'')+' '+doc


        writer = csv.writer(wf)
        writer.writerow(['asin','reviewText'])
        for key in asin_dict:
            l=[]
            l.append(key)
            l.append(asin_dict[key])
            writer.writerow(l)


def removePunctuation(document):
    return document.replace(',','').replace('.','').replace(':','').replace(';','').replace('(','').replace(')','').replace('"','').replace('!','').replace('?','').lower()

# proprecess('../../dataset/reviews_Amazon_Instant_Video.json')
readcsv('../../dataset/aiv_all_removed_stop_words.csv')
# simpleCount('../../dataset/aiv.csv')

# removeStopWords('../../dataset/aiv_all.csv')