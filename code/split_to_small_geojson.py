import pathlib
import geopandas as gpd
import os
from tqdm import tqdm

def export_block_geojsons(shape_dir, export_dir):
    shapes = sorted(pathlib.Path(shape_dir).glob('*.zip'))

    for county_file in tqdm(shapes):
        gdf = gpd.read_file(county_file)
        state = gdf['GEOID20'].str[:2].values[0]
        os.system('mkdir -p %s' % os.path.join(export_dir,state))
        for bg in tqdm(gdf['GEOID20'].str[:12]):
            pdf = gdf[gdf['GEOID20'].str[:12] == bg]
            pdf.to_file(os.path.join(os.path.join(export_dir,state), '%s.geojson' % bg))
        
        # Small routine updates
        os.system("git add -A && git commit -m 'adding %s' && git pull && git push" % county_file.name)

if __name__=='__main__':
    shapefile_dir = '../../national_address_database/data/shapefiles'
    export_dir = '../data/'
    os.system('mkdir -p %s' % export_dir)
    assert os.path.isdir(shapefile_dir)
    assert os.path.isdir(export_dir)
    export_block_geojsons(shapefile_dir, export_dir)