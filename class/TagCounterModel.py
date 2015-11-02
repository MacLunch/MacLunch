import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs


class TagCounterModel:
  def get_tag(self, dataframe, is_tf = False):
    num_df = len(dataframe)

    tag_list = []
    for text in dataframe:
        tags = {}

        soup = bs(text, 'html.parser')

        soup_col = [tag.name for tag in soup.find_all()]

        if is_tf == False:
          for tag in soup.find_all():
              tag_name = 'TAG_' + tag.name

              if tag_name not in tags:
                  tags[tag_name] = 0

              tags[tag_name] += 1

          tag_list.append(tags)
        else:
          for tag in self.tag_col:
              tag_name = 'TAG_' + tag

              if tag_name not in tags:
                tags[tag_name] = 0

              if tag in soup_col:
                tags[tag_name] += 1

          tag_list.append(tags)

    df = pd.DataFrame.from_dict(tag_list)
    df = df.fillna(0)
    df.index = dataframe.index

    return df

  def fit_transform(self, dataframe):
    df = self.get_tag(dataframe)
    self.tag_col = df.columns

    return df

  def fit(self, dataframe):
    df = self.get_tag(dataframe)
    self.tag_col = df.columns

  def transform(self, dataframe):
    df = self.get_tag(dataframe, is_tf = True)
    return df

  def get_col(self):
    return self.tag_col

  def set_col(self, columns):
    self.tag_col = columns