import numpy as np
import pandas as pd
from sklearn.feature_extraction import FeatureHasher

class FeatureHasherModel:
	def fit(self, max_features):
		self.model = FeatureHasher(input_type = "string", n_features = max_features)

	def transform(self, dataframe, col_name):
		hashed = self.model.transform(dataframe)

		df = pd.DataFrame(hashed.toarray())
		df.columns = ["%s_%d" % (col_name, author_num) for author_num in range(0, self.model.n_features)]

		return df

	def get_model(self):
		return self.model

	def set_model(self, model):
		self.model = model