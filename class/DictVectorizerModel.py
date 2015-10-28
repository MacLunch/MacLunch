import numpy as np
import pandas as pd
from sklearn.feature_extraction import DictVectorizer

class DictVectorizerModel:
	def fit(self, train):
		temp_list = []

		for item in train:
		    dic = {"dict" : item}
		    temp_list.append(dic)


		self.model = DictVectorizer()
		self.model.fit(temp_list)

	def transform(self, dataframe, col_name):
		temp_list = []
		for item in dataframe:
			dic = {"dict" : item}
			temp_list.append(dic)

		df = self.model.transform(temp_list).toarray()
		df = pd.DataFrame(df)
		df.index = dataframe.index

		df.columns = ["%s_%d" % (col_name, data) for data in df.columns]

		return df

	def get_model(self):
		return self.model

	def set_model(self, model):
		self.model = model