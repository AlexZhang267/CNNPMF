# coding=utf-8
import numpy as np
import csv
import sys
csv.field_size_limit(sys.maxsize)

class Tfidf:
    def __init__(self):
        self.weighted = False
        self.documents = []
        self.corpus_dict = {}

    def addDocument(self, doc_name, list_of_words):
        # building a dictionary
        doc_dict = {}
        for w in list_of_words:
            # print w
            doc_dict[w] = doc_dict.get(w, 0.) + 1.0
            self.corpus_dict[w] = self.corpus_dict.get(w, 0.0) + 1.0

        # normalizing the dictionary
        length = float(len(list_of_words))
        for k in doc_dict:
            # calculate tf
            doc_dict[k] = doc_dict[k] / length

        # add the normalized document to the corpus
        self.documents.append([doc_name, doc_dict, list_of_words])

    def idf(self):

        self.word_idf_dict={}
        self.word_df_dict={}    # document frequency
        length = self.documents.__len__()
        #calculate the number of papers w where occur in
        for doc in self.documents:
            doc_dict = doc[1]
            for w in doc_dict:
                self.word_idf_dict[w] = self.word_idf_dict.get(w,0) + 1

        for w in self.word_idf_dict:
            self.word_df_dict[w] = self.word_idf_dict.get(w,1)/length
            self.word_idf_dict[w] = np.log(length / self.word_idf_dict.get(w, 1))

    def tfidf(self):
        #取一个word最大的tfidf作为这个word的tfidf值,无论其处于哪篇文档
        self.word_tfidf_dict={}
        for doc in self.documents:
            doc_dict = doc[1]
            for w in doc_dict:
                doc_dict[w] = doc_dict[w]*self.word_idf_dict.get(w, 0)
                tmp = self.word_tfidf_dict.get(w,0)
                if tmp < doc_dict[w]:
                    self.word_tfidf_dict[w] = doc_dict[w]

    def similarities(self, list_of_words):
        """Returns a list of all the [docname, similarity_score] pairs relative to a list of words."""

        # building the query dictionary
        query_dict = {}
        for w in list_of_words:
            query_dict[w] = query_dict.get(w, 0.0) + 1.0

        # normalizing the query
        length = float(len(list_of_words))
        for k in query_dict:
            query_dict[k] = query_dict[k] / length

        # computing the list of similarities
        sims = []
        for doc in self.documents:
            score = 0.0
            doc_dict = doc[1]
            for k in query_dict:
                if k in doc_dict:
                    score += (query_dict[k] / self.corpus_dict[k]) + (doc_dict[k] / self.corpus_dict[k])
            sims.append([doc[0], score])

        return sims


def proprecess():
    dict_reader = csv.DictReader(open('../../dataset/aiv_removed_stop_words_5.csv','r'))
    count = 0
    tfidf = Tfidf()
    for row in dict_reader:
        count += 1
        # if count > 10:
        #     break
        tfidf.addDocument(row['asin'],row['reviewText'].split())

    # print('there are %d items'%(count))
    tfidf.idf()
    tfidf.tfidf()

    # print tfidf.word_tfidf_dict

    tfidf_dict = sorted(tfidf.word_tfidf_dict.iteritems(), key=lambda d: d[1], reverse=True)
    # print dict
    #get top 8000 words
    top8000_tfidf_dict = dict(tfidf_dict[0:8000])
    print top8000_tfidf_dict
    print len(top8000_tfidf_dict)
    # with open('../../dataset/top_8000_words_5.csv','a') as wf:
    #     writer = csv.writer(wf)
    #     writer.writerow(['word','wcore'])
    #     for d in dict:
    #         writer.writerow(d)
        # writer.writerow(list(d) for d in dict)

    count = 0
    with open('../../dataset/aiv_data_5core.csv','a') as wf:
        writer = csv.writer(wf)
        writer.writerow(['asin','reviewText'])
        for doc in tfidf.documents:
            count +=1
            # if count>5:
            #     break
            reviewWordList = doc[2]
            cleanReviewText = []
            cleanReviewText.append(doc[0])
            words=''
            for word in reviewWordList:
                if word in top8000_tfidf_dict and tfidf.word_df_dict.get(word,0)<0.5:
                    words+=word+' '
            cleanReviewText.append(words)
            # print cleanReviewText
            writer.writerow(cleanReviewText)



if __name__=='__main__':
    proprecess()