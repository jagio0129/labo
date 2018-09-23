# coding: UTF-8
import pandas as pd
from collections import defaultdict
from lib.DataProvider import user
from tqdm import tqdm

# 施設一覧
def facility_list(data_frame):
  return data_frame['type2'].unique()

# カテゴリ一覧
def category_list(data_frame):
  return data_frame['type1'].unique()

# 各施設にどのくらい人が訪れているか
## 1ユーザが複数ヶ所訪れても同様にカウントする
def facility_rate(data_frame):
  print("Count visiting to how facility")
  d = defaultdict(int)
  ul = user.user_list(data_frame)
  pbar = tqdm(total=len(ul))
  for u in ul:
    user_df = data_frame[data_frame['user_id'] == u]
    fl = category_list(user_df)
    for f in fl:
      d[f] += 1
    pbar.update(1)
  pbar.close()
  return d

# 各施設にどのくらい人が訪れているか
## 1ユーザが複数ヶ所訪れても同様にカウントする
def category_rate(data_frame):
  print("Count visiting to how facility")
  d = defaultdict(int)
  ul = user.user_list(data_frame)
  pbar = tqdm(total=len(ul))
  for u in ul:
    user_df = data_frame[data_frame['user_id'] == u]
    fl = facility_list(user_df)
    for f in fl:
      d[f] += 1
    pbar.update(1)
  pbar.close()
  return d
