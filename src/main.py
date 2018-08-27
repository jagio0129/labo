# coding: UTF-8

import sys
sys.dont_write_bytecode = True
import pandas as pd
import time
import os
import geocoder
from collections import defaultdict
import csv
import branca
from tqdm import tqdm

from lib import utils
from lib.DataProvider import basic
from lib.DataProvider import user_id
from lib.DataProvider import sex
from lib.DataProvider import geometory as geo
from lib.DataProvider import date
from lib import mymap

### files
# 2013-07-01.csv, 2013-07-07.csv, 2013-10-07.csv,
# 2013-10-13.csv, 2013-12-16.csv, 2013-12-22.csv

FOLDER = "/home/vagrant/mount_folder/lab/data/person_trip"
TEST_FOLDER = ["/home/vagrant/mount_folder/lab/data/person_trip/2013-07-07.csv"]
MESH_SUFFIX = "_onMesh.csv"
GEO_JSON = "/home/vagrant/mount_folder/lab/data/geojson/syutoken.geojson"
SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

class Main:
    
  def __init__(self, abs_file):
    self.gen_mesh_csv(abs_file)

    # 時間をdatetime型にキャスト
    self.df['date'] = pd.to_datetime(self.df['date'])

    # 一時間ごと24個のDateTimeオブジェクトを生成
    file = os.path.basename(abs_file)
    self.byH = date.gen_by_date(
      utils.file_date(file),
      24,
      "H"
    )
    
  # メッシュコードを追加した新規CSVファイルを生成する。
  def gen_mesh_csv(self, abs_file):
    file = os.path.basename(abs_file)
    root, ext = os.path.splitext(file)
    new_file = FOLDER + "/" + root + MESH_SUFFIX
    if os.path.isfile(new_file):
      print("Skip create " + new_file)
      self.df = pd.read_csv(new_file)
    else:
      print("Create " + new_file)
      self.df = pd.read_csv(abs_file)
      self.df = geo.add_meshcode_column(self.df)
      self.df.to_csv(new_file, index=False)

### main
if __name__ == '__main__':
  start = time.time()

  os.chdir(FOLDER)
  
  #for abs_file in utils.file_list(FOLDER):
  for abs_file in TEST_FOLDER:
    print("File: " + abs_file)
    main = Main(abs_file)
    df = main.df
    byH = main.byH

    extra_df = date.data_by_timerange_on_user_id(df, byH[15], user_id.list(df))
    extra_df.index = range(1,len(extra_df)+1)

    if not os.path.isfile(SOURCE_PATH + "/number_of_city_15.csv"):
      city_dict = defaultdict(int)
      pbar = tqdm(total=len(extra_df))
      for row in extra_df.itertuples():
        lat = row.latitude
        lon = row.longitude
        city = mymap.get_city_form_geocoder(lat, lon, 0)
        time.sleep(0.5)
        city_dict[city] += 1
        pbar.update(1)
      pbar.close()

      city_df = pd.DataFrame(list(city_dict.items()),columns=['city','number'])
      city_df.to_csv(SOURCE_PATH + "/number_of_city_15.csv")

    mymap.mygen_geojson_map(GEO_JSON, SOURCE_PATH + "/number_of_city_15.csv", SOURCE_PATH)


  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")