# coding: UTF-8

import pandas as pd
from tqdm import tqdm

# 一定時間ごとのDateTimeオブジェクトを生成
def gen_by_date(start, periods, freq):
  return pd.date_range(
    start  + " 00:00:00",
    periods=periods,
    freq=freq
  )

# 指定した時間帯のデータを抽出
def get_term_data(data_frame,date_range):
  # 指定時間範囲のデータを抽出
  return data_frame[str(date_range):str(date_range+1)]

# 指定した時間帯のデータから、一番時間の早いデータだけをユーザごとに抽出
##  指定した時間帯のデータがない場合は、一番近い時間帯のデータを抽出する
def get_first_data(data_frame, date_range, user_list):
  print("Extra "+ str(date_range) + " ~ " + str(date_range + 1) + " data")
  # indexをdatetime型に変換
  data_frame.set_index('date', inplace=True)
  
  all_df = pd.DataFrame()
  pbar = tqdm(total=len(user_list))
  for user in user_list:
    exist_f = True
    cnt = 1
    user_df = data_frame[data_frame['user_id'] == user]
    extra_df = get_term_data(user_df, date_range)
    while(len(extra_df) == 0):
      extra_df = get_term_data(user_df, date_range - cnt)
      if((date_range - cnt).hour == 0):
        break
      cnt += 1
    if(exist_f):
      all_df = pd.concat([all_df, extra_df.head(1)])
    else:
      all_df = pd.concat([all_df, extra_df.tail(1)])
    pbar.update(1)
  pbar.close()

  # インデックスをintに変更
  all_df.index = range(1,len(all_df)+1)
  return all_df
