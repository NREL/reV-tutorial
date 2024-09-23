reV generation
===========================

This tutorial focuses on the **generation** module of the NREL reV model. 
When running reV, a series of JSON files are used to inform the model on what configs you want to use and where you want to use them.
Throughout the pipeline there are configs that are required and ones that are optional.
All of the steps in the pipeline require execution control.
This tutorial includes a **configuration JSON** file (`config_gen.json`) that specify the simulation parameters, including system specifications, time periods, output requests, etc. 
This example module runs at several points in Rhode Island for 2012 and 2013 NSRDB data. 

The `config_gen.json` specifies file locations of files that generated from previous tutorials, including:

- **Project points**: It specifies the geographical locations (lat/lon) where the generation module will be performed. 
- **Resource data**: This is typically in HDF5 format that contains solar (NSRDB) or wind (WTK) data. 
- **SAM configurations**: The "sam_files" entry contains a set of key-value pairs which represent the "config" column in the project points file and the SAM configuration associated with it.

Add entry descriptions here:
- `project_points`: "../data/project_points/rhode_island_onshore_solar_project_points.csv",
- `resource_file`: "../data/resources/ri_100_NSRDB_{}.h5",


Simply run the following command in your terminal:

```
reV generation -c config_gen.json
```

To explore more command options, use the `--help` flag: 

```
reV generation --help
```
