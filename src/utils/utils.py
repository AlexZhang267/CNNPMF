#coding=utf-8
import csv

def getIDAsinDict():
    fin = open('../dataset/aiv_ratings_5core.csv', 'r')
    reviewerNum = 0
    asinNum = 0
    reviewerDict = {}
    asinDict = {}
    reader_dict = csv.DictReader(fin)

    for row in reader_dict:
        if row['reviewerID'] not in reviewerDict:
            reviewerDict[row['reviewerID']] = reviewerNum
            reviewerNum += 1

        if row['asin'] not in asinDict:
            asinDict[row['asin']] = asinNum
            asinNum += 1

    return reviewerDict,asinDict