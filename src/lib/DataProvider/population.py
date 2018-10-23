# coding: UTF-8

import pandas as pd
import codecs

# 市区町村の人口を返す
def population(population_csv_path, area_code):
  if area_code == "None":
    raise

  pop = 0
  # csvファイルが綺麗な形でなかったためcodecsを使用
  with codecs.open(population_csv_path, "r", "Shift-JIS", "ignore") as file:
    df = pd.read_table(file, delimiter=",") 
    area_df = df[df["地域コード"] == int(area_code)]

    # 指定した地域コードのデータがなければ処理を止める
    if len(area_df) == 0:
      raise("GeoJSONに含まれる地域の人口データが存在しません")

    pop = area_df["人口　総数"].values[0]
  return pop