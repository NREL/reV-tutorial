"""Upload existing geotiffs into a new or existing reV-compatible HDF5 file."""
import os

from reVX.utilities.exclusions_converter import ExclusionsConverter


# Target file
EXCL_FPATH = "./RI_Exclusions.h5"
O_EXCL_FPATH = os.path.abspath("../../data/ri_exclusions.h5")

# Datasets to upload
LAYER_FPATHS = {
 'ri_padus': 'ri_padus.tif',
 'ri_reeds_regions': 'ri_reeds_regions.tif',
 'ri_smod': 'ri_smod.tif',
 'ri_srtm_slope': 'ri_srtm_slope.tif'
}

LAYER_DESCS = {
 'ri_padus': 'Protected Lands Dataset US.',
 'ri_reeds_regions': 'ReEDS Regions.',
 'ri_smod': 'Global Human Settlement Layer - Settlement Model',
 'ri_srtm_slope': 'SRTM-derived slope.'
}


def geotiffs_to_h5():
    """Upload geotiff to a new or existing h5 file."""
    ExclusionsConverter.layers_to_h5(
        excl_h5=EXCL_FPATH,
        layers=LAYER_FPATHS,
        descriptions=LAYER_DESCS
    )


def h5_to_geotiffs():
    """Pull h5 datasets out as a geotiff."""
    converter = ExclusionsConverter(O_EXCL_FPATH)
    for layer in converter.layers:
        if layer not in ["latitude", "longitude"]:
            if "techmap" not in layer:
                dst = "./" + layer + ".tif"
                converter.layer_to_geotiff(layer, dst)


if __name__ == "__main__":
    geotiffs_to_h5()