#coding=utf-8
import csv
import json
def proprecess(jsonfile):
    file = open(jsonfile,'r')
    count = 0

    with open('../../dataset/aiv.csv','a') as wf:
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
    with open('../../dataset/aiv.csv','r') as f:
        dict_reader = csv.DictReader(f)
        for row in dict_reader:
            print(row['reviewerID'])
            print(row['overall'])


proprecess('../../dataset/reviews_Amazon_Instant_Video_5.json')
# readcsv('../../dataset/aiv.csv')