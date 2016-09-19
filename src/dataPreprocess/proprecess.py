#coding=utf-8
import csv
import json
import sys
import numpy as np
import matplotlib.pyplot as plt
import random

csv.field_size_limit(sys.maxsize)
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

def simpleCount():
    with open('../../dataset/aiv_ratings_5core.csv','r') as f:
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

def countLens():
    dict_reader = csv.DictReader(open('../../dataset/aiv_data_5core_length_50.csv','r'))
    lenList=[]
    for row in dict_reader:
        lenList.append(len(row['reviewText'].split()))

    lenList = np.asarray(lenList)
    max = np.max(lenList)
    min = np.min(lenList)

    fig,ax = plt.subplots()
    ax.hist(lenList,max-min+1)
    plt.show()

def combine(csvfilw):
    f = open(csvfilw,'r')
    dict_reader = csv.DictReader(f)
    count = 0



    with open('../../dataset/aiv_combine_5.csv','a') as wf:
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


def removeStopWords():
    f2 = open('../../dataset/stopwords.txt', 'r')
    stopwords = []
    for line in f2:
        stopwords.append(' '+line.strip()+' ')

    dict_reader = csv.DictReader(open('../../dataset/aiv_combine_5.csv','r'))
    count = 0
    with open('../../dataset/aiv_removed_stop_words_5.csv','a') as wf:
        writer = csv.writer(wf)
        writer.writerow(['asin','reviewText'])
        for row in dict_reader:
            # count += 1
            # if count > 10:
            #     break
            # print row['asin'], row['reviewText']
            for s in stopwords:
                row['reviewText'] = row['reviewText'].replace(s,' ')
            # print row['asin'],row['reviewText']
            l=[]
            l.append(row['asin'])
            l.append(row['reviewText'])
            writer.writerow(l)



def storeRating():
    with open('../../dataset/aiv_ratings_5core.csv','a') as wf:
        writer=csv.writer(wf)
        writer.writerow(['reviewerID','asin','overall'])
        reader_dict = csv.DictReader(open('../../dataset/aiv.csv','r'))
        for row in reader_dict:
            l=[]
            l.append(row['reviewerID'])
            l.append(row['asin'])
            l.append(row['overall'])
            writer.writerow(l)

def buildCorpus():
    s = ""
    reader_dict = csv.DictReader(open('../../dataset/aiv.csv','r'))
    for row in reader_dict:
        s += removePunctuation(row['reviewText'])+' '

    with open('../../dataset/corpus_5core.csv','a') as wf:
        print len(s)
        wf.write(s)

def buildTopWordsVectors5core():
    dict_reader = csv.DictReader(open('../../dataset/top_8000_words_5.csv','r'))
    fin = open('../../dataset/vectors.txt','r')
    vectors_dict={}
    for line in fin:
        tmp = line.split(' ',1)
        vectors_dict[tmp[0]] = tmp[1].replace("\r\n",'').replace('\n','')
    with open('../../dataset/top_8000_words_vectors_5core.csv','a') as wf:
        writer = csv.writer(wf)
        writer.writerow(['word','vector'])
        for row in dict_reader:
            if row['word'] in vectors_dict:
                writer.writerow([row['word'],vectors_dict[row['word']]])
    fin.close()

def buildTopWordsVectors5coreWithInitialize():
    dict_reader = csv.DictReader(open('../../dataset/top_8000_words_5.csv','r'))
    fin = open('../../dataset/vectors.txt','r')
    vectors_dict={}
    for line in fin:
        tmp = line.split(' ',1)
        vectors_dict[tmp[0]] = tmp[1].replace("\r\n",'').replace('\n','')
    with open('../../dataset/top_8000_words_vectors_5core_with_initialization.csv','a') as wf:
        writer = csv.writer(wf)
        writer.writerow(['word','vector'])
        for row in dict_reader:
            if row['word'] in vectors_dict:
                writer.writerow([row['word'],vectors_dict[row['word']]])
            else:
                writer.writerow([row['word'],str(np.random.uniform(-0.5,0.5,50)).replace('\r\n','').replace('\n','').replace('[','').replace(']','')])
    fin.close()



def generateData():
    fin = open('../../dataset/aiv_ratings_5core.csv','r')
    reviewerNum = 0
    asinNum = 0
    reviewerDict={}
    ratingList=[]
    asinDict={}
    reader_dict = csv.DictReader(fin)

    for row in reader_dict:
        if row['reviewerID'] not in reviewerDict:
            reviewerDict[row['reviewerID']] = reviewerNum
            reviewerNum+=1

        if row['asin'] not in asinDict:
            asinDict[row['asin']] = asinNum
            asinNum+=1

        tmp=''
        tmp += str(reviewerDict[row['reviewerID']])+" "
        tmp += str(asinDict[row['asin']])+" "
        tmp += str(row['overall'])
        ratingList.append(tmp)

    random.shuffle(ratingList)
    length = len(ratingList)
    flag = int(length*0.8)
    trainData = ratingList[:flag]
    validationData = ratingList[flag:]

    # print (trainData)
    # print(validationData)

    trainWriter = csv.writer(open('../../dataset/train_data.csv','a'))
    validationWriter = csv.writer(open('../../dataset/validation_data.csv','a'))
    for d in trainData:
        trainWriter.writerow(d.split())
    for dd in validationData:
        validationWriter.writerow(dd.split())









if __name__=='__main__':
    # proprecess('../../dataset/reviews_Amazon_Instant_Video.json')
    # readcsv('../../dataset/aiv_data_5core.csv')
    # storeRating()
    # simpleCount()
    # countLens()
    # buildCorpus()
    # buildTopWordsVectors5coreWithInitialize()
    generateData()
    # combine('../../dataset/aiv.csv')
    # removeStopWords('../../dataset/aiv_all.csv')
    # removeStopWords()