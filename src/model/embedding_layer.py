#coding=utf-8
import numpy as np
import csv
'''
词向量已经由glove得到
embedding layer只需要将文档转化为已有的vector然后作为下一层的输入
有的词没有vector,就随机分配吧,先搭一个model再说
'''
class EmbeddingLayer(object):
    def __init__(self,documents):
        '''
        :param documents:a mini batch size list of documents
        '''
        self.out = np.asarray(np.zeros((len(documents),50,50)))
        doccount = 0

        reader_dict = csv.DictReader(open('../dataset/top_8000_words_vectors_5core_with_initialization.csv','r'))
        word_dict={}
        for row in reader_dict:
            word_dict[row['word']] = np.array(row['vector'].split())
            assert len(word_dict[row['word']])==50


        print len(documents)
        for doc in documents:
            # the document length should be 50
            print doc
            print len(doc.split())
            assert len(doc.split())==51
            doc=doc.split()[1:]
            print doc
            vectors=np.zeros((50,50))
            wordcount = 0
            for word in doc:
                vectors[wordcount]=word_dict[word]
                wordcount+=1
            assert wordcount==50
            self.out[doccount]=vectors
            doccount+=1






