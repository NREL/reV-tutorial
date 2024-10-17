Build exclusion data
===
This folder introduces you how to build reV-compatible high resolution 
land-use `HDF5` datasets used for exclusions and characterizations.
The exclusion data format is an `HDF5` collection of data arrays with 
attribute information (descriptive metadata) stored. For example, the values 
within the arrays indicate whether a grid cell is excluded (`1` for excluded, 
`0` for non-excluded) based on the specific exclusion layer such as protected 
land areas (details see below). The metadata 
provide descriptions of the exclusion criteria, sources of exclusion data, and 
other information that help in identifying the purposes of each type of
 exclusion. Please refer back to the 
[2_resource_data/](../../tutorial_03_input_builds/2_resource_data/) folder 
in this tutorial_03 for an overview of the structure of `HDF5` 
format data. The exclusion data developed here will eventually be accessed in the 
`config_aggregation.json` file. Please see 
[tutorial_06_aggregation](../../tutorial_06_aggregation/) for further information. 


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
- **Protected areas**: Protected Lands Dataset in the USA ("ri_padus.tif"). 
- [ReEDS](https://www.nrel.gov/analysis/reeds/): The Regional Energy 
Deployment System Regions ("ri_reeds_regions.tif"). 
- [Human Settlement](https://human-settlement.emergency.copernicus.eu): 
Global Human Settlement Layer ("ri_smod.tif"). 
- **Elevation**: SRTM-derived slope ("ri_srtm_slope.tif"). 

Other exclusion data may include urban areas that are heavily developed or 
urbanized, infrastructures that are unsuitable for development, etc. 

You can also add any number of descriptive attributes, 
such as creation date, source, citation, etc., to each dataset 
using the `h5py` library. To learn more information on `h5py` and its uses,  
please see the [h5py help doc](https://docs.h5py.org/en/stable/quick.html#core-concepts).

