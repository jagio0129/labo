# coding: UTF-8
import os
import time
import pandas as pd
from lib.DataProvider import gravity

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

    ary = []
    user_df = df[df.user_id == 2000].head(2)
    for row in user_df.itertuples():
      ary.append(row)

    rowA = ary[0]
    rowB = ary[1]

    posA = [rowA.latitude, rowA.longitude]
    posB = [rowB.latitude, rowB.longitude]

    distAB = gravity.dist_on_sphere(posA, posB)
    print(distAB)

  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
