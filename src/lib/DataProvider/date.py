# coding: UTF-8

import pandas as pd

# 一定時間ごとのDateTimeオブジェクトを生成
def gen_by_date(start, periods, freq):
  return pd.date_range(
    start  + " 00:00:00",
    periods=periods,
    freq=freq
  )