### environment
ubuntu 16.04
Python 3.6.5
pip    18.1

### set up 
```
sudo apt-get install apache2 gdal-bin libbz2-dev -y
sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
pip3 install --user git+https://github.com/geopandas/geopandas/
pip3 install --user pandas jupyter geopy descartes python-geohash tqdm geocoder folium shapely python3-matplotlib
cp config.ini.skeleton config.ini  # config.iniを適切に修正
```

### 行政区画データの入手先
http://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v2_3.html

### GeoJSONファイルの結合
```
ogr2ogr -f GeoJSON -append <結合されるファイル> <結合するファイル>
```

### mapデータの確認
```
python3 plot_map.py
```

ブラウザから`localhost/cgi-bin/index.rb`にアクセス

### 各プログラムの説明
- facility_main.py
  - 各施設をどのくらいのユーザが訪れたか算出する
- gravity_main.py
  - 流動データをグラビティモデルに適応する
- od_main.py
  - 全ODデータから流動量を算出
- plot_map.py
  - GeoJSONなどをmapにプロットする
- population_main.py
  - 国勢調査から市区町村ごとの人口を抽出
