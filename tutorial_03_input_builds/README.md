# Building/Finding reV Inputs

For a full model pipeline, as far as input datasets go, reV requires the following files: 

1) A SAM configuration JSON
    - Refer to the two methods in `1_sam_configs/` to build a SAM config file.
    - This file will be used in the [tutorial_04_generation_a/](../tutorial_04_generation_a/), and [tutorial_05_pipeline/](../tutorial_05_pipeline/). 
2) Resource data HDF5 files
    - Resource files that are required to be compatible with `reV` runs.
3) A project points CSV file
    - A sample Python script in `3_project_points/` will introduce you how to create project points.
4) An exclusion HDF5 file
    - A sample Python script and raster files in `4_exclusion_data/` will introduce how to create HDF5 datasets for exclusions. 
5) A transmission connection CSV table
    - Introduce you to the transmission table that is used in the reV supply-curve-aggregation. 

Optionally, there are various points in the model pipeline where you can override constant input parameters with site specific parameters.

In each of these folders, you will find a README explaining how the input building script works.
