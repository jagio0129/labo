## 各スクリプトの概要
### facility_main.py
各施設にどのくらいのユーザが立ち寄るかを取得できる

### gravity_main.py
データをグラビティモデルに適応する

## od_main.py
ユーザがどこからどこへ行くのかを取得する

## plot_main.py
流動データやGeoJSONなどをマップにプロットする。

## population_main.py
国税調査データから該当する地域の人口だけを抽出


## データの設置
Google Driveのデータをdata配下に設置する

## config
```
cp config.ini.skeleton config.ini
```

## cgiスクリプトの設置
`/usr/lib/cgi-bin`にindex.rbを設置する