# coding: UTF-8

import re
import glob
import json

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