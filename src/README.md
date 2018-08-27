### environment
ubuntu 16.04
Python 3.6.5

### set up 
```
sudo apt-get install apache2 gdal-bin -y
sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
pip3 install --user git+https://github.com/geopandas/geopandas/
pip3 install --user pandas jupyter geopy descartes python-geohash tqdm geocoder folium
```

### run
`python3 main.py`

### 行政区画データの入手先
http://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v2_3.html

### GeoJSONファイルの結合
```
ogr2ogr -f GeoJSON -append <結合されるファイル> <結合するファイル>
```

### mapデータの確認
```
python3 plot_map.py
sudo mv syutoken.html /var/www/html/
```

ブラウザから`localhost/syutoken.html`にアクセス
