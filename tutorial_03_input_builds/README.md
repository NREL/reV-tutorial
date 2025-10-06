# Building/Finding reV Inputs



For a full model pipeline, reV requires at least the following inputs: 

1) **A SAM Configuration JSON File**
    - This refers to reV-compatible configurations for the System Advisor Model (SAM), which is used to simulate energy generation and costs.
    - Refer to the two methods in `1_sam_configs/` to build a SAM config file.
    - This file will be used in the [tutorial_04_generation_a/](../tutorial_04_generation_a/), and [tutorial_05_pipeline/](../tutorial_05_pipeline/). 
3) **Resource Data HDF5 Files**
    - "Resource" here refers to spatial timeseries of atmospheric or geothermal energy resources.
    - HDF5 refers to Hierarchical Data Format, Version 5, which is the data format required for reV's generation module.
    - The datasets stored in these files require a very specific structure.
    - These can built manually if you have resource data in another format or may accessed remotely through NREL's API or AWS S3 bucket.
5) **A Project Points CSV File**
    - This refers to a table that instructs reV where to run SAM configurations.
    - A sample Python script in `3_project_points/` will introduce you how to create these.
7) **An Exclusion HDF5 File**
    - The exclusion file is used in the `supply-curve-aggregation` module, which will be used to model available land and capacity for different technologies.
    - A sample Python script and raster files in `4_exclusion_data/` will introduce how to create HDF5 datasets for exclusions. 
8) **A Transmission Connection CSV File**
    - This refers to a table of supply curve points representing potential power generation sites and their potential interconnection tie-line distances and costs.
    - Building this table may be more or less complex, but regardless of which level of detail is desired a more extensive build tutorial will be needed.
    - Introduce you to the transmission table that is used in the reV supply-curve-aggregation. 

In each of these folders, you will find a README explaining how to either obtain or build each of these inputs.
