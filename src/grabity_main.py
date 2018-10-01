# coding: UTF-8
import os
import time
import pandas as pd
from tqdm import tqdm

from lib import utils
from lib.DataProvider import gravity
from lib.DataProvider import user
from lib.DataProvider import geo
from lib.DataProvider import date
from lib.DataProvider import facility as fc
from lib.Viewer import map as mymap

### files
# 2013-07-01.csv, 2013-07-07.csv, 2013-10-07.csv,
# 2013-10-13.csv, 2013-12-16.csv, 2013-12-22.csv

ROOT_PATH = "/home/vagrant/mount_folder/lab"
DATA_PATH = ROOT_PATH + "/data"
PERSON_TRIP = DATA_PATH + "/person_trip"
CHOROPLETH = DATA_PATH + "/choropleth"
GEO_JSON = DATA_PATH + "/geojson/syutoken.geojson"
SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

TEST_FOLDER = [PERSON_TRIP + "/2013-07-01.csv"]

### main
if __name__ == '__main__':

  start = time.time()

  for abs_file in TEST_FOLDER:  # テスト用

    # csvファイルをDataFrameとしてロード
    df = pd.read_csv(abs_file)

    # ユーザごとに以下の処理を行う
    u_list = user.user_list(df)
    pbar = tqdm(total=len(u_list))
    for u in u_list:
      
      # ユーザのODを取得
      od_df = user.get_start_end_and_stay(df, u)
      
      # ODを一度配列に格納
      ary = []
      for row in od_df.itertuples():
        ary.append(row)
      
      # レコードごとに以下の処理を行う
      for i in range(0, len(ary), 1):
        if i+1 == len(ary):
          break
        
        # レコードを２つ取得
        rowA, rowB = ary[i], ary[i+1]
        # それぞれのレコードの位置情報を取得
        latlonA, latlonB = [rowA.latitude, rowA.longitude], [rowB.latitude, rowB.longitude]
        
        # それぞれの市区町村名を取得
        geo_json = utils.json_parser(GEO_JSON)
        city_nameA = geo.belong(geo_json,latlonA[0],latlonA[1])
        city_nameB = geo.belong(geo_json,latlonB[0],latlonB[1])

        # ２点間が同一市区町村”でない”なら以下の処理
        if not city_nameA == city_nameB:

          # ２点間の距離を取得
          distAB = gravity.dist_on_sphere(latlonA, latlonB)
          print(distAB)

        pbar.update(1)
      pbar.close()  

  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
