# coding: UTF-8
import pandas as pd
from collections import defaultdict
from tqdm import tqdm

from lib.DataProvider import user

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

# 指定ユーザの最初のレコードと、STAY状態のデータフレームを返す
#   return >DataFrame>
def orgin_and_stay(data_frame, user_id):
  user_df = data_frame[data_frame['user_id'] == user_id]
  # レコードのheadを取得
  start = user_df.head(1)
  # 状態がSTAYのレコードを取得
  stay = user_df[user_df['status'] == "STAY"]
  # 上記３つを結合
  user_df = pd.concat([start,stay])
  # 重複レコードを削除
  od_df = user_df[~user_df.duplicated()]
  return od_df  

# 指定ユーザの最初と最後のレコードに加えて、STAY状態のデータフレームを返す
#   return <DataFrame>
def get_start_end_and_stay(data_frame, user_id):
  
  user_df = data_frame[data_frame['user_id'] == user_id]

  # レコードのheadを取得
  start = user_df.head(1)
  # 状態がSTAYのレコードを取得
  stay = user_df[user_df['status'] == "STAY"]
  # レコードのtailを取得
  end = user_df.tail(1)
  
  # 上記３つを結合
  user_df = pd.concat([start,stay,end])
  # 重複レコードを削除
  od_df = user_df[~user_df.duplicated()]
  return od_df

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

# 一日で一箇所の施設に滞在したユーザかどうか
def is_stop_one_point_user(data_frame, user_id):
  # indexのフリ直し
  df = data_frame[data_frame['user_id'] == user_id].reset_index()
  
  # 先頭行と末尾行除く
  new_df = df.drop([0, len(df)-1])
  
  # レコード数が1以下ならreturn
  if len(new_df.index) <= 1:
    return False

  # statusにMOVEしか含まないならreturn
  if set(new_df.status.unique()) == set(["MOVE"]):
    return False
  
  # STAYレコードを1つだけ含むユーザを抽出
  if new_df.status.value_counts()["STAY"] == 1:
    return True
  return False

# 一日で一箇所の施設に滞在したユーザのid一覧
def stop_one_point_user_ids(data_frame):
  mList = []
  uList = user.user_list(data_frame)
  pbar = tqdm(total=len(uList))  # for progress bar
  for id in uList:
    if is_stop_one_point_user(data_frame, id):
      mList.append(id)
    pbar.update(1)
  pbar.close()
  return sorted(mList)
