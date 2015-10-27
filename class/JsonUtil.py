import numpy as np
import pandas as pd
import json
import jpype
import glob
from random import shuffle
from bs4 import BeautifulSoup as bs
from konlpy.tag import Mecab

class JsonUtil:
	def parse(self, data_path = "data"):
		file_list = glob.glob("%s/*.json" % data_path)
		json_list=[]

		shuffle(file_list)
		for json_file_name in file_list:
			json_file = json.loads(open(json_file_name).read())
			json_list += json_file["articles"]

		mecab = Mecab()

		dataframe = []

		for cnt, article in enumerate(json_list):

			text = bs(article["text"], "html.parser").text
			title_pos = ["%s_%s" % (word, pos) for word, pos in mecab.pos(article["title"])]
			author_pos = ["%s_%s" % (word, pos) for word, pos in mecab.pos(article["author"])]
			text_pos = ["%s_%s" % (first, second) for first, second in mecab.pos(text)]

			dataframe.append({
                "title_pos": title_pos,
                "title_pos_sentences" : " ".join(title_pos),
                "author_pos": author_pos,
                "author_pos_sentences" : " ".join(author_pos),
                "text":article["text"],
                "text_pos": text_pos,
                "text_pos_sentences" : " ".join(text_pos),
                "forumid": article["forumid"],                    
                "istroll": article["is_troll"],
                "pk": article["pk"]
			})

		dataframe = pd.DataFrame.from_dict(dataframe)
		dataframe = dataframe.set_index("pk")

		return dataframe