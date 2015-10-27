import numpy as np
import pandas as pd
from gensim.models import word2vec

class Word2VecModel:
    def make_feature_vec(self, words, model, num_features):
        feature_vec = np.zeros((num_features,), dtype = "float32")
        
        nwords = 0
        
        index2word_set = set(model.index2word)
        
        for word in words:
            if word in index2word_set:
                nwords = nwords + 1.
                feature_vec = np.add(feature_vec, model[word])
        
        if nwords != 0:
            feature_vec = np.divide(feature_vec, nwords)
        
        return feature_vec

    def get_avg_feature_vecs(self, texts, model, num_features):
        counter = 0
        
        text_feature_vecs = np.zeros((len(texts), num_features), dtype = "float32")
        
        for i, text in enumerate(texts):
            
            if i % 10000 == 0:
                print(i)
            
            text_feature_vecs[i] = self.make_feature_vec(text , model, num_features)
            
        return text_feature_vecs

    def fit(self, train, max_features):
        min_word_count = 40
        num_workers = -1
        context = 40
        downsampling = 1e-3

        min_word_count = min(min_word_count, len(train))
        context = min(context, len(train))

        sentences = train.apply(lambda x:" ".join(x))

        self.model = word2vec.Word2Vec(sentences, workers = num_workers, size = max_features, \
                                min_count = min_word_count, window = context, sample = downsampling)
        self.max_features = max_features

    def transform(self, dataframe, col_name):
        col = ["word2vec_%s_%d" % (col_name, data) for data in range(0, self.max_features)]
        
        df_word2vec = self.get_avg_feature_vecs(dataframe, self.model, self.max_features)
        df_word2vec = pd.DataFrame(df_word2vec, index = dataframe.index, columns = col)
        
        return df_word2vec

    def get_model(self):
        return self.model

    def set_model(self, model):
        self.model = model
        self.max_features = model.syn0.shape[1]
