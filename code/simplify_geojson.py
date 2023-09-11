import geopandas as gpd
import pathlib
from tqdm import tqdm


if __name__ == "__main__":
    data_files = sorted(pathlib.Path("../data").glob("*.geojson"))
    pbar = tqdm(data_files)

    dic = {}

    for d in pbar:
        pbar.set_description(str(d))
        # Geoid reference: https://www.census.gov/programs-surveys/geography/guidance/geo-identifiers.html
        gdf = gpd.read_file(d)
        gdf = gdf[["geometry"]]
        gdf.to_file(d)
