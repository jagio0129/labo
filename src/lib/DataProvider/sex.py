# coding: UTF-8

from lib.DataProvider import user_id
from collections import defaultdict

# sexの種類を返す
def list(data_frame):
  return data_frame['sex'].unique()

# 各性別が何人いるのか
def rate(data_frame):
  d = defaultdict(int)
  for user in user_id.list(data_frame):
    user_df = data_frame[data_frame['user_id'] == user].head(1)
    sex_type = user_df['sex'].values[0]
    d[sex_type] += 1
  return d