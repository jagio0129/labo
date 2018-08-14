# coding: UTF-8

import pandas as pd

# 指定ユーザの最初と最後のレコードだけのデータフレームを返す
def get_start_end(user_data_frame):
  return pd.concat([user_data_frame.head(1),user_data_frame.tail(1)])

# 指定ユーザの最初と最後のレコードに加えて、STAY状態のデータフレームを返す
def get_start_end_and_stay(user_data_frame):
  start = user_data_frame.head(1)
  stay = user_data_frame[user_data_frame['status'] == "STAY"]
  end = user_data_frame.tail(1)
  return pd.concat([start,stay,end])

# 各csvファイルのdfをdf_list(dict)に格納
def data_frame_list(file_list):
  print("reading...")
  df_list = {}
  for f_path in file_list:
    print("\t%s " % f_path)
    df_list["%s" % f_path] = pd.read_csv(f_path)
  print("Finish!")
  return df_list