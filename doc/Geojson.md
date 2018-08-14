# Geojson
位置情報を持つJSON形式のデータを指す。具体的には以下のようなデータ構造を持つ

```json
{ "type":"FeatureCollection",
	"features": [
		{ "type": "Feature",
		   "geometry": {
			"type": "Point",
			"coordinates": [102.0, 0.5]
		    },
      		   "properties": {"prop0": "value0"}
		},
    		{ "type": "Feature",
      		   "geometry": {
        		"type": "LineString",
        		"coordinates": [
          			[102.0, 0.0], [103.0, 1.0]
          		]
        	    },
      		    "properties": {
        		"prop0": "value0",
        		"prop1": 0.0
        	    }
		},
     	]
}
```

Geojsonオブジェクトは次の3種類で表現する
- ジオメトリ(形状)
- フューチャー(地物)
- フューチャーコレクション

### ジオメトリオブジェクト
`type`が次のいずれか
- Point
- MultiPoin
- LineString
- MultiLineStrin
- Polygo
- MultiPolygon
- GeometryCollection

### フューチャーオブジェクト
`type`がFeature。必ずgeometry,propertiesのメンバーを持つ。内容はそれぞれジオメトリオブジェクトかJSONのNull、任意のJSONオブジェクトかJSONのNull。
"properties"メンバーには、国や県の名前などを入れることが多いらしい。

### フューチャーコレクションオブジェクト
`type`がFeatureCollection。フィーチャーオブジェクトの集まり。"features" に対応する値は配列。