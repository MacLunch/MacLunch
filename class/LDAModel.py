import numpy as np
import pandas as pd
import gensim
from gensim import corpora, models
from gensim.corpora import TextCorpus, MmCorpus, Dictionary
from nltk.corpus import stopwords
from optparse import OptionParser

class LDAModel:
    def fit(self, train, keep_n, num_topics):

        dictionary = corpora.Dictionary(train)

        dictionary.filter_extremes(keep_n=keep_n)

        corpus = [dictionary.doc2bow(text) for text in train]

        self.model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, chunksize=1000, passes=1)

    def transform(self, dataframe, keep_n, col_name):

        dictionary = corpora.Dictionary(dataframe)

        dictionary.filter_extremes(keep_n=keep_n)

        corpus = [dictionary.doc2bow(text) for text in dataframe]

        num = len(dataframe)
        df = []
        
        for i in range(0,num):
            if i % 10000 == 0:
                print(i)
            
            temp = [i[1] for i in self.model.get_document_topics(corpus[i],minimum_probability=0)]
            df.append(temp)
        
        col = ["lda_%s_%d" % (col_name, data) for data in range(0, self.model.num_topics)]
        df = pd.DataFrame(df, columns = col)
        df.index = dataframe.index

        return df

    def get_model(self):
        return self.model

    def set_model(self, model):
        self.model = model