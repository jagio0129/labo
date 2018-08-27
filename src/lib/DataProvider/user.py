# coding: UTF-8
import pandas as pd
from collections import defaultdict

# ユーザ一覧
def user_list(data_frame):
  return data_frame['user_id'].unique()

# 存在しないuser_idの一覧を表示する
#   return <dict>
def show_not_exist(data_frame):
  ul = user_list(data_frame)
  ul.sort()

  i = 0
  num = []
  for id in ul:
    if not (i in ul):
      while (i != int(id)):
        num.append(i)
        i += 1
    i += 1
  print("No exist UserID:")
  print(num)
  print("Size: %d" % len(num))

# 指定ユーザの最初と最後のレコードだけのデータフレームを返す
#   return <DataFrame>
def get_start_end(data_frame, user_id):
  user_df = data_frame[data_frame['user_id'] == user_id]
  return pd.concat([user_df.head(1),user_df.tail(1)])

# 指定ユーザの最初と最後のレコードに加えて、STAY状態のデータフレームを返す
#   return <DataFrame>
def get_start_end_and_stay(data_frame, user_id):
  user_df = data_frame[data_frame['user_id'] == user_id]
  start = user_df.head(1)
  stay = user_df[user_df['status'] == "STAY"]
  end = user_df.tail(1)
  return pd.concat([start,stay,end])

# sexの種類を返す
#   return <dict>
def sex_list(data_frame):
  return data_frame['sex'].unique()

# 各性別が何人いるのかをdictに格納
#   return <dict>
def sexies_rate(data_frame):
  d = defaultdict(int)
  for user in user_list(data_frame):
    user_df = data_frame[data_frame['user_id'] == user].head(1)
    sex_type = user_df['sex'].values[0]
    d[sex_type] += 1
  return d