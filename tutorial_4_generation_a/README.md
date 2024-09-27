reV generation
===========================

This tutorial focuses on the **generation** module of the NREL reV model. 
When running reV, a series of JSON files are used to inform the model on what configs you want to use and where you want to use them.
Throughout the pipeline there are configs that are required and ones that are optional.
All of the steps in the pipeline require execution control.
This tutorial includes a **configuration JSON** file (`config_gen.json`) that specify the simulation parameters, including system specifications, time periods, output requests, etc. 
This example module runs at several points in Rhode Island for 2012 and 2013 NSRDB data. 

The `config_gen.json` entries that correspond to the input data created in `tutorial_3_input_builds/` are described below: 

1) `sam_files`: The location of [SAM configurations](../tutorial_3_input_builds/1_sam_configs/) file that we created. 
    - A set of key-value pairs which represent the "config" column in the project points file and the SAM configuration associated with it.
2) `resource_file`: The location of [resource data](../tutorial_3_input_builds/2_resource_data/) is typically in HDF5 format that contains solar (NSRDB) or wind (WTK) data. 
    - Since we are executing `reV` from the command line, this input string can contain brackets `{}` that will be filled in by the `analysis_years` entry (in this case, year 2012 and 2013).
    - Alternatively, this input can be a list of explicit files to process. In this case, the length of the list must match the length of the `analysis_years` input exactly, and the path are assumed to align with the analysis_years (i.e. the first path corresponds to the first analysis year, the second path corresponds to the second analysis year, and so on).
3) `project_points`: The [project points](../tutorial_3_input_builds/3_project_points/) file location. 
    - It specifies the geographical locations (lat/lon) where the generation module will be performed. 

You need to change the config file locations for all above entries in the `config_gen.json`. Other brief descriptions to the entries are listed below; check on the [reV generation help doc](https://nrel.github.io/reV/_cli/reV%20generation.html) for further documentations on each: 

- `log_directory`: Path to directory where logs should be written. Path can be relative and does not have to exist on disk (it will be created if missing). In our case, we created the logs at the current directory: `"./logs/"`. 
- `execution_control`: Dictionary containing execution control arguments. 
- `log_level`: String representation of desired logger verbosity. Suitable options are `DEBUG` (most verbose), `INFO` (moderately verbose), `WARNING` (only log warnings and errors), and `ERROR` (only log errors).
- `technology`: String indicating which SAM technology to analyze. We use `pvwattsv8`.

After the configurations, to run the generation, simply run the following command in your terminal:

```console
local:tutorial_4_generation_a user$ reV generation -c config_gen.json
```

To explore more command options, use the `--help` flag: 

```
reV generation --help
```
