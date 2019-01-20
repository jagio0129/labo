# coding: UTF-8

import re
import glob
import json
import pandas as pd

# 実データ(yyyy-mm-dd.csv)だけを絶対パスのlistで返す
def file_list(folder):
  l = glob.glob(folder + "/*")
  data = [v for v in l if re.search('[\d]{4}-[\d]{2}-[\d]{2}.csv', v)]
  paths = [path for path in data]
  return paths

# ファイル名から日付を取得
#   return <str(yyyy-mm-dd)>
def file_date(file):
  return file.split("/")[-1].split(".")[0]

# json用整形プリンター
def jprint(data):
  print(json.dumps(data, indent=2))

# jsonをパース
def json_parser(json_path):
  f = open(json_path,'r')
  return json.load(f)

# 処理の概要をdumpする
def dump_description(destination):
  hash_str = ""
  for i in range(len(destination)+4):
    hash_str += "#"
  print(hash_str)
  print("# %s #" % destination)
  print(hash_str)

# 全日のデータを統合して返す
def all_df(folder):
  all_df = pd.concat([pd.read_csv(abs_file) for abs_file in file_list(folder)])
  return all_df