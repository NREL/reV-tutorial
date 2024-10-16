Build exclusion data
===
This folder introduces you how to build reV-compatible high resolution 
land-use `HDF5` datasets used for exclusions and characterizations.
The exclusion data format is an `HDF5` collection of data arrays with 
attribute information (descriptive metadata) stored. Specifically, the values 
within the arrays indicate whether a grid cell is excluded (`1` for excluded, 
`0` for non-excluded) based on the specific exclusion layer used. The metadata 
provide descriptions of the exclusion criteria, sources of exclusion data, and 
other information that help in identifying the purposes of each type of
 exclusion. Please refer back to the 
[2_resource_data/](../../tutorial_03_input_builds/2_resource_data/) folder 
in this tutorial_03 for an overview of the structure of `HDF5` 
format data. 


The Python file `exclusion.py` provides steps to upload existing geotiffs 
into a new or existing reV-compatible `HDF5` file. The script uses `reVX`, 
which stands for 
[reV eXchange tool](https://github.com/NREL/reVX/tree/main?tab=readme-ov-file). 
The `reVX` already has methods that 
handle the conversion and we are going to use in this tutorial. 


There are several exclusion datasets in `*.tif` format that are used as example 
exclusion layer inputs. The file paths of these datasets are included in a 
dictionary `LAYER_FPATHS`. 
The corresponding descriptions for these datasets are 
included in a dictionary `LAYER_DESCS`. The first function `geotiffs_to_h5()` 
then upload geotiffs to a new or existing h5 file. 
The second function `h5_to_geotiffs()` pulls existing 
HDF5 datasets out as a geotiff.
Some of the commonly used exclusion 
layers that reflect constraints on development are:
- Protected areas: Protected Lands Dataset in the USA ("ri_padus.tif"). 
- The Regional Energy Deployment System 
([ReEDS](https://www.nrel.gov/analysis/reeds/)) Regions ("ri_reeds_regions.tif"). 
- Global Human Settlement Layer - Settlement Model ("ri_smod.tif"). 
- SRTM-derived slope ("ri_srtm_slope.tif"). 
- Urban areas that are heavily developed or urbanized. 
- Infrastructures that are unsuitable for development.

You can also add any number of descriptive attributes, 
such as creation date, source, citation, etc., to each dataset 
using the `h5py` library. To learn more information on `h5py` and its uses,  
please see the [h5py help doc](https://docs.h5py.org/en/stable/quick.html#core-concepts).


Things to do (x)
===
- Describe generally what the format is (An HDF5 collection of arrays with attribute information)
- Describe how you start with GeoTiffs
- The data in the GeoTiff can represent anything, you'll handle how to interpret the values
  in a later configuration file
- Describe how reVX already has methods that handle the conversion and link to it.
- Also describe how you can any number of descriptive attributes to each dataset using H5py (creation date, source, citation, etc.)
