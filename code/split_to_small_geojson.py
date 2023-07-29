import pathlib
import geopandas as gpd
import os
from tqdm import tqdm
import fiona

def export_block_geojsons(shape_dir, export_dir):
    shapes = sorted(pathlib.Path(shape_dir).glob('*.zip'))

    pbar = tqdm(shapes)
    state = '01'
    for county_file in pbar:
        current_state = county_file.name[:2]
        if current_state != state:
            os.system("git add -A && git commit -m 'adding %s' && git pull && git push" % county_file.name)
            state = current_state
        try:
            gdf = gpd.read_file(county_file)
            county = gdf['GEOID20'].str[:5].values[0]
            pbar.set_description('Updating county: %s' % county)
            # Assuming if a directory is there, the directory is valid
            if os.path.isdir(os.path.join(export_dir,county)):
                continue
            os.system('mkdir -p %s' % os.path.join(export_dir,county))
            updated = 0
            for bg in tqdm(gdf['GEOID20'].str[:12].unique()):
                export_filename = os.path.join(os.path.join(export_dir,county), '%s.geojson' % bg)
                if os.path.isfile(export_filename):
                    continue
                pdf = gdf[gdf['GEOID20'].str[:12] == bg]
                pdf.to_file(export_filename)
                updated += 1
        except Exception as e:
            # Ran into driver error, skipping and deleting base shapefile and the export dir
            print('Removing: %s' % county_file.resolve())
            os.system('rm %s' % county_file.resolve())
            os.system('rm -rf %s' % os.path.join(export_dir,county))
            continue


if __name__=='__main__':
    shapefile_dir = '../../national_address_database/data/shapefiles'
    export_dir = '../data/'
    os.system('mkdir -p %s' % export_dir)
    assert os.path.isdir(shapefile_dir)
    assert os.path.isdir(export_dir)
    export_block_geojsons(shapefile_dir, export_dir)