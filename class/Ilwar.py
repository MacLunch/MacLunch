
# coding: utf-8

# In[1]:
from sklearn.feature_extraction.text import CountVectorizer

def make_bag_of_words(labeled_train, max_features, col_name, vectorizer):
    
    train_data_features = vectorizer.transform(labeled_train[col_name]).toarray()

    col = ["bow_%s_%s" % (col_name, data) for data in vectorizer.get_feature_names()]
    df_bow = pd.DataFrame(train_data_features, columns = col, index=labeled_train.index)
    
    labeled_train = pd.concat([labeled_train, df_bow],axis=1)
    
    return labeled_train


def fit_bag_of_words(labeled_train, max_features, col_name):
    vectorizer = CountVectorizer(analyzer = "word", tokenizer = None, preprocessor = None,
                                stop_words = None, max_features=max_features)
    vectorizer.fit(labeled_train[col_name])
        
    return vectorizer

# In[3]:

from gensim.models import word2vec

def make_feature_vec(words, model, num_features):
    
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

def get_avg_feature_vecs(texts, model, num_features):
    
    counter = 0
    
    text_feature_vecs = np.zeros((len(texts), num_features), dtype = "float32")
    
    for i, text in enumerate(texts):
        
        if i % 10000 == 0:
            print(i)
        
        text_feature_vecs[i] = make_feature_vec(text , model, num_features)
        
    return text_feature_vecs

def fit_word2vec(train, col_name, max_features):
    num_features = max_features
    min_word_count = 40
    num_workers = -1
    context = 40
    downsampling = 1e-3

    sentences = " ".join(train[col_name].apply(lambda x:" ".join(x)))

    min_word_count = min(min_word_count, len(train[col_name]))
    context = min(context, len(train[col_name]))

    model = word2vec.Word2Vec(sentences, workers = num_workers, size = num_features,                             min_count = min_word_count, window = context, sample = downsampling)

    return model

def make_word2vec(train, col_name, max_features, model):
    col = ["word2vec_%s_%d" % (col_name, data) for data in range(0, max_features)]
    
    train_feature = get_avg_feature_vecs(train[col_name].apply(lambda x:" ".join(x)), model, max_features)
    train_feature = pd.DataFrame(train_feature, index = train.index, columns = col)
    
    train = pd.concat([train, train_feature], axis = 1)
    
    return train

# In[6]:

from konlpy.tag import Mecab
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
import json
import jpype
import glob
from random import shuffle
from bs4 import BeautifulSoup as bs
from sklearn import preprocessing

class TrollClassifier:
    def __init__(self, path):
        self.train_path = path
    def set_train_path(self, path):
        self.train_path = path
    def fit(self):
        file_list = glob.glob("%s/*.json" % self.train_path)
        shuffle(file_list)
        json_train=[]

        for json_file_name in file_list:
            json_file = json.loads(open(json_file_name).read())
            json_train += json_file["articles"]
    
        mecab = Mecab()

        labeled_train = []

        for cnt, article in enumerate(json_train):
            if cnt % 10000 == 0:
                print(cnt)
                
            text = bs(article["text"], "html.parser").text
            title_pos = ["%s_%s" % (word, pos) for word, pos in mecab.pos(article["title"])]
            author_pos = ["%s_%s" % (word, pos) for word, pos in mecab.pos(article["author"])]
            text_pos = ["%s_%s" % (first, second) for first, second in mecab.pos(text)]

            labeled_train.append({
                "istroll": article["is_troll"],
                "title_pos": title_pos,
                "title_pos_sentences" : " ".join(title_pos),
                "author_pos": author_pos,
                "author_pos_sentences" : " ".join(author_pos),
                "text_pos": text_pos,
                "text_pos_sentences" : " ".join(text_pos),
                "forumid": article["forumid"],                    
                "pk": article["pk"]
            })

        labeled_train = pd.DataFrame.from_dict(labeled_train)
        labeled_train = labeled_train.set_index('pk')
        
        self.author_model = fit_word2vec(labeled_train, "author_pos", 600)
        self.title_model = fit_bag_of_words(labeled_train, 500, "title_pos_sentences")
        self.text_model = fit_bag_of_words(labeled_train, 500, "text_pos_sentences")

        labeled_train = make_word2vec(labeled_train, "author_pos", 600, self.author_model)
        labeled_train = make_bag_of_words(labeled_train, 500, "title_pos_sentences", self.title_model)
        labeled_train = make_bag_of_words(labeled_train, 500, "text_pos_sentences", self.text_model)

        le = preprocessing.LabelEncoder()

        labeled_train["forumid"] = le.fit_transform(labeled_train["forumid"])
        
        label = 'istroll'
        pre = labeled_train.columns.drop(['author_pos', 'author_pos_sentences'                                          ,'title_pos', 'title_pos_sentences',                                          'text_pos', 'text_pos_sentences', label])
        
        self.model = RandomForestClassifier(n_estimators=10, n_jobs=-1)
        self.model.fit(labeled_train[pre],labeled_train[label])
        
        print("fit complete")
        
    def predict_file(self, path):
        json_file = json.loads(open(path).read())
        json_test = json_file["articles"]
        
        mecab = Mecab()
        test = []
        article = json_test[1]

        text = bs(article["text"], "html.parser").text
        title_pos = ["%s_%s" % (word, pos) for word, pos in mecab.pos(article["title"])]
        author_pos = ["%s_%s" % (word, pos) for word, pos in mecab.pos(article["author"])]
        text_pos = ["%s_%s" % (first, second) for first, second in mecab.pos(text)]
        
        test.append({
            "title_pos": title_pos,
            "title_pos_sentences" : " ".join(title_pos),
            "author_pos": author_pos,
            "author_pos_sentences" : " ".join(author_pos),
            "text_pos": text_pos,
            "text_pos_sentences" : " ".join(text_pos),
            "forumid": article["forumid"],                    
            "pk": article["pk"]
        })
        
        test = pd.DataFrame(test)
        test = test.set_index("pk")

        le = preprocessing.LabelEncoder()

        test["forumid"] = le.fit_transform(test["forumid"])

        test = make_word2vec(test, "author_pos", 600, self.author_model)
        test = make_bag_of_words(test, 500, "title_pos_sentences", self.title_model)
        test = make_bag_of_words(test, 500, "text_pos_sentences", self.text_model)

        pre = test.columns.drop(['author_pos', 'author_pos_sentences','title_pos', 'title_pos_sentences','text_pos', 'text_pos_sentences'])
        
        result = self.model.predict_proba(test[pre])
        #result=0
        
        return result


# In[ ]:



