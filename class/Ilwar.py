from konlpy.tag import Mecab
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
import json
import jpype
import glob
import os
from random import shuffle
from bs4 import BeautifulSoup as bs
from sklearn import preprocessing
from xgboost.sklearn import XGBClassifier
import pickle

from JsonUtil import JsonUtil
from DictVectorizerModel import DictVectorizerModel
from Word2VecModel import Word2VecModel
from BagOfWordsVectorizer import BagOfWordsVectorizer
from FeatureHasherModel import FeatureHasherModel
from LDAModel import LDAModel
from TagCounterModel import TagCounterModel

class TrollClassifier:
    def set_train_path(self, path):
        self.train_path = path

    def pre_process(self, json, istrain):
        mecab = Mecab()

        data = []

        for cnt, article in enumerate(json):
            if cnt % 10000 == 0:
                print(cnt)
                
            text = bs(article["text"], "html.parser").text
            #title_pos = ["%s_%s" % (word, pos) for word, pos in mecab.pos(article["title"])]
            #author_pos = ["%s_%s" % (word, pos) for word, pos in mecab.pos(article["author"])]
            text_pos = ["%s_%s" % (first, second) for first, second in mecab.pos(text)]

            data.append({
                #"title_pos": title_pos,
                #"title_pos_sentences" : " ".join(title_pos),
                #"author_pos": author_pos,
                #"author_pos_sentences" : " ".join(author_pos),
                "text":article["text"],
                "text_pos": text_pos,
                "text_pos_sentences" : " ".join(text_pos),
                #"forumid": article["forumid"],                    
                "pk": article["pk"]
            })

            if istrain == True:
                data[cnt]["istroll"] = article["is_troll"]

        data = pd.DataFrame.from_dict(data)
        data = data.set_index('pk')

        return data

    def fit(self, json_train, n_estimators = 10, is_xgb = True):

        train = self.pre_process(json_train, istrain = True)
        
        bow_vectorizer = BagOfWordsVectorizer()
        word2vec_model = Word2VecModel()
        tag_counter_model = TagCounterModel()

        # word2vec_model.fit(train["author_pos_sentences"], 500)
        # author_features = word2vec_model.transform(train["author_pos_sentences"], "author")
        # self.author_model = word2vec_model.get_model()

#        bow_vectorizer.fit(train["title_pos_sentences"], 1000)
#        title_features = bow_vectorizer.transform(train["title_pos_sentences"], "title")
#        self.title_model = bow_vectorizer.get_vectorizer()

        bow_vectorizer.fit(train["text_pos_sentences"], 1000)
        text_features = bow_vectorizer.transform(train["text_pos_sentences"], "text")
        self.text_model = bow_vectorizer.get_vectorizer()

#        tag_features = tag_counter_model.fit_transform(train["text"])
#        self.tag_model = tag_counter_model.get_col()

        train = pd.concat([train, text_features], axis = 1)

        #le = preprocessing.LabelEncoder()

        # train["forumid"] = le.fit_transform(train["forumid"])
        
        label = train['istroll']
        train = train.drop('istroll', axis=1)
        train = train.drop(['text', 'text_pos', 'text_pos_sentences'], axis=1)
        
        print(train.columns)

        train.columns = [str(x) for x in range(len(train.columns))]
        
        if is_xgb == False:
            self.model = RandomForestClassifier(n_estimators, n_jobs=-1)
        else:
            self.model = XGBClassifier(n_estimators = n_estimators, max_depth = 10)

        print(train.shape)
        self.model.fit(train, label)

    def save_model(self, save_path = "predict_model"):

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        #pickle.dump(self.author_model, open("%s/author_model.p" % save_path, "wb"), protocol = pickle.HIGHEST_PROTOCOL)
        #pickle.dump(self.title_model, open("%s/title_model.p" % save_path, "wb"), protocol = pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.text_model, open("%s/text_model.p" % save_path, "wb"), protocol = pickle.HIGHEST_PROTOCOL)
        #pickle.dump(self.tag_model, open("%s/tag_model.p" % save_path,"wb"), protocol = pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.model, open("%s/predict_model.p" % save_path,"wb"), protocol = pickle.HIGHEST_PROTOCOL)

    def load_model(self, save_path = "predict_model"):
        #self.author_model = pickle.load(open("%s/author_model.p" % save_path, "rb"))
        #self.title_model = pickle.load(open("%s/title_model.p" % save_path, "rb"))
        self.text_model = pickle.load(open("%s/text_model.p" % save_path, "rb"))
        #self.tag_model = pickle.load(open("%s/tag_model.p" % save_path, "rb"))
        self.model = pickle.load(open("%s/predict_model.p" % save_path,"rb"))

    def _predict(self, json_test):
        
        test = self.pre_process(json_test, istrain = False)

        bow_vectorizer = BagOfWordsVectorizer()
        word2vec_model = Word2VecModel()
        tag_counter_model = TagCounterModel()

        # word2vec_model.set_model(self.author_model)
        # author_features = word2vec_model.transform(test["author_pos_sentences"], "author")

        #bow_vectorizer.set_vectorizer(self.title_model)
        #title_features = bow_vectorizer.transform(test["title_pos_sentences"], "title")

        bow_vectorizer.set_vectorizer(self.text_model)
        text_features = bow_vectorizer.transform(test["text_pos_sentences"], "text")

        #tag_counter_model.set_col(self.tag_model)
        #tag_features = tag_counter_model.transform(test["text"])

        test = pd.concat([test, text_features], axis = 1)

        #le = preprocessing.LabelEncoder()

        #test["forumid"] = le.fit_transform(test["forumid"])

        test = test.drop(['text', 'text_pos', 'text_pos_sentences'], axis=1)

        test.columns = [str(x) for x in range(len(test.columns))]

        return test

        
    def predict(self, json_test):
        result = self.model.predict(self._predict(json_test))
        
        return result

    def predict_proba(self, json_test):
        result = self.model.predict_proba(self._predict(json_test)).T

        #if results are all False, it's not 2-dimensional so return only first col

        if result.shape[0] < 2:
            return result[0]
        else:
            return result[1]

