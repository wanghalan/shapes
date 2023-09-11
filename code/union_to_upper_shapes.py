import geopandas as gpd
import pathlib
from tqdm import tqdm
from shapely.ops import unary_union


def store_union_key(dic, geoid, length, gdf):
    key = geoid[:length]
    polygons = []
    if key in dic:
        polygons = dic[key]

    polygons = polygons.extend(gdf["geometry"])
    boundary = gpd.GeoSeries(unary_union(polygons))
    dic[key] = boundary


if __name__ == "__main__":
    data_files = sorted(pathlib.Path("../data").glob("**/*.geojson"))
    pbar = tqdm(data_files)

    dic = {}

    for d in pbar:
        pbar.set_description(str(d))

        # Geoid reference: https://www.census.gov/programs-surveys/geography/guidance/geo-identifiers.html
        gdf = gpd.read_file(d)
        store_union_key(dic, d.stem, 5, gdf)  # county
        store_union_key(dic, d.stem, 11, gdf)  # census tract
    
    # After the unions are generated
    for key in dic:
        
