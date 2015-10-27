import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

class BagOfWordsVectorizer:
    def transform(self, dataframe, col_name):
        data_features = self.vectorizer.transform(dataframe).toarray()

        col = ["bow_%s_%s" % (col_name, data) for data in self.vectorizer.get_feature_names()]
        df_bow = pd.DataFrame(data_features, columns = col, index=dataframe.index)

        return df_bow


    def fit(self, train, max_features):
        self.vectorizer = CountVectorizer(analyzer = "word", tokenizer = None, preprocessor = None,\
                                    stop_words = None, max_features=max_features)

        self.vectorizer.fit(train)

    def get_vectorizer(self):
        return self.vectorizer

    def set_vectorizer(self, vectorizer):
        self.vectorizer = vectorizer