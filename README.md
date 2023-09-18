# shapes

A collection of encoded shapefiles

1. Converting shapefiles to geojson files
```bash
# cd code/
python parallel_split_geojson.py
```
2. Converting geojson files topojson files
```bash
# npm install -g topojson 
for file in *.geojson; do              
        geo2topo "${file}" > "$(basename -- "$file" .geojson).topojson"
done
```
3. Gunzipping topojson files
```bash
gzip data/*
```
