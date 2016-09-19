#coding=utf-8
import csv
import utils
def load_train_data():
    pass

def load_validation_data():
    pass

def loadDocuments():
    reviewerIDDict, asinDict = utils.getIDAsinDict()
    reader_dict = csv.DictReader(open('../dataset/aiv_data_5core_length_50.csv','r'))
    documentList=[]
    num_not_50=0
    num_50=0
    for row in reader_dict:
        if not len(row['reviewText'].split())==50:
            print (row['asin'],'document length is',len(row['reviewText'].split()))
            num_not_50+=1
        else:
            documentList.append(str(asinDict[row['asin']])+' '+row['reviewText'])
            num_50+=1
    print('not 50 count ',num_not_50)
    print('50 count',num_50)

    return documentList
