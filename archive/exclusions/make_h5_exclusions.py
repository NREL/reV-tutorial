import h5py
import json
import matplotlib.pyplot as plt
from revruns.rreformatter import Reformatter



# Get the inputs that you want to add to the H5 File
INPUTS = { 
    "esri_fedlands": {
        "path": "esri_fedlands.tif"
    },
    "conus_padus_excl":{
        "path": "conus_padus_excl.tif"
    },
    "sage_grouse":{
        "path": "sage_grouse_habitat.gpkg"
    }
} 
# Out directory for the rasters
OUT_DIR = 'outputs'
# Path to the Exclusions file
EXCL_FPATH = 'example_exclusions.h5'

# Run the function 
def main():
    ref = Reformatter(INPUTS, OUT_DIR, 'all_fed_lands_excl.tif', EXCL_FPATH, overwrite_tif=True)
    ref.main()


if __name__ == "__main__":
    main()
#     self = Reformatter(INPUTS, OUT_DIR, '/shared-projects/rev/projects/geothermal/fy23/data/rasters/county_fips.tif', EXCL_FPATH)

