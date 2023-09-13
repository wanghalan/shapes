import pathlib
import geopandas as gpd
from tqdm import tqdm
import pandas as pd
import os
import multiprocessing
from os import listdir
import csv
from pqdm.processes import pqdm
import time


def process_file(file):
    geoid = file.stem.split("_")[2]
    export_filename = "../data/{geoid}.geojson".format(geoid=geoid)
    if os.path.isfile(export_filename):
        return True

    gdf = gpd.read_file(file)
    gdf = gdf[["GEOID20", "geometry"]]
    gdf.to_file(export_filename, index=False)
    return True


if __name__ == "__main__":
    shapefile_dir = "../../national_address_database/data/shapefiles"
    export_dir = "../data/"

    bdfs = []
    shape_files = sorted(pathlib.Path(shapefile_dir).glob("*.zip"))
    result = pqdm(shape_files, process_file, n_jobs=multiprocessing.cpu_count())
    print(result)
