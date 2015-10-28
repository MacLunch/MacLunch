import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
from html.parser import HTMLParser as hp
import html
import copy


#text가 bs로 파싱되어있지 않아야 되는데, 저희 쪽에선 이미 파싱되서 들어오므로 쓸지 안쓸지는 모르겠네영
#일단 만들어두긴 합니다
class TagCounterModel:
  def get_tag(self, dataframe):
    num_df = len(dataframe)

    tag_list = []
    for text in dataframe:
        tags = {}

        soup = bs(text, 'html.parser')

        for tag in soup.find_all():
            tag_name = 'TAG_' + tag.name

            if tag_name not in tags:
                tags[tag_name] = 0

            tags[tag_name] += 1

        tag_list.append(tags)

    df = pd.DataFrame.from_dict(tag_list)
    df = df.fillna(0)
    df.index = dataframe.index

    return df