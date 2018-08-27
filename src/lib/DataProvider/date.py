# coding: UTF-8

import pandas as pd

# 一定時間ごとのDateTimeオブジェクトを生成
def gen_by_date(start, periods, freq):
  return pd.date_range(
    start  + " 00:00:00",
    periods=periods,
    freq=freq
  )

# 指定した時間帯のデータを抽出
def get_term_data(data_frame,date_range):
  # indexをdatetime型に変換
  data_frame.set_index('date', inplace=True)
  # 指定時間範囲のデータを抽出
  return data_frame[str(date_range):str(date_range+1)]

# 指定した時間帯のデータから、一番時間の早いデータだけをユーザごとに抽出
def get_first_data(data_frame, date_range, user_list):
  df = get_term_data(data_frame,date_range)
  all_df = pd.DataFrame()
  # 各user_idの先頭だけ抽出
  for user in user_list:
    extra_df = df[df['user_id']==user].head(1)
    all_df = pd.concat([all_df, extra_df])
  return all_df

