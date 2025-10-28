reV generation
===========================

This tutorial focuses on the **generation** module of the NREL reV model. When running reV, a series of JSON files are used to inform the model on what configuration files you want to use and where you want to use them.Throughout the pipeline there are configs that are required and ones that are optional. All of the steps in the pipeline require execution control. This tutorial includes a **configuration JSON** file (`config_gen.json`) that specify the simulation parameters, including system specifications, time periods, output requests, etc. This example module runs at several points in Rhode Island for 2012 and 2013 NSRDB data.

The `config_generation.json` entries that correspond to the input data created in `tutorial_3_input_builds/` are described below: 

1) `technology`: A string representing the SAM module you wish to run.
    - Not all SAM generation modules are available. Available modules include "pvwattsv5", "pvwattsv7", "pvwattsv8", "Pvsamv1", "tcsmolten_salt", "solarwaterheat", "lineardirectsteam", "geothermal", "windpower", and "mhkwave".
2) `sam_files`: The key and location of your System Advisor Model (SAM) configuration file (or files). 
    - A set of key-value pairs which correspond to the "config" column in the project points file and the path to the SAM configuration file associated with it.
3) `project_points`: The path to a project points file. 
    - This input specifies the geographical locations (lat/lon) where the generation module will be performed. This file may also contain spatially-explicit SAM parameters by providing a new column named after the target SAM parameter.
4) `resource_file`: One or multiple paths to your resource HDF5 file(s) corresponding with the chosen technology module.
    - This input may be a single string for a single resource file, a list that contains the full path to multiple resource files you want to run, or a single string with a set of brackets (`{}`) that will be filled in by the `analysis_years` entry (in this case, year 2012 and 2013).
5) `output_request`: A list of strings representing the datasets you wish to be written to the output reV HDF5 generation file.
    - This may be include both reV derived variables and SAM parameters if it is useful to pass those through.
    <pre>
    "output_request": [
      "cf_mean", <a href="https://nrel.github.io/reV/_autosummary/reV.SAM.generation.PvWattsv8.html#reV.SAM.generation.PvWattsv8.cf_mean"># Description</a>
      "cf_profile", <a href="https://nrel.github.io/reV/_autosummary/reV.SAM.generation.PvWattsv8.html#reV.SAM.generation.PvWattsv8.cf_profile"># Description</a>
      "lcoe_fcr", <a href="https://nrel.github.io/reV/_autosummary/reV.SAM.econ.LCOE.html#reV.SAM.econ.LCOE.lcoe_fcr"># Description</a>
      "ghi_mean", <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.Outputs.gh"># Description</a>
      "ghi_profile", <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.Outputs.gh"># Description</a>
    ]</pre>
- `log_directory`: Path to directory where logs should be written. Path can be relative and does not have to exist on disk (it will be created if missing). In our case, we created the logs at the current directory: `"./logs/"`. Each log file will be named after the process ID of the job. Information logging and uncaught errors will be writted to a file with the `.o` extension. Warnings and errors will be logged to a separate `.e` file.
- `execution_control`: Dictionary containing execution control arguments. 
- `log_level`: String representation of desired logger verbosity. Suitable options are "DEBUG" (most verbose) and "INFO" (moderately verbose). 

Note that the "_mean" in the output requests (for example, in the `cf_mean`) indicates time-averaged results calculated by SAM. 

Before running the first reV generation module, it is essential to readdress the relationship between `reV` and `SAM` to better understand the interplay mechanism of these two systems. The `reV` modeling framework acts as a high-level pipeline, utlizing `SAM` for detailed performance and financial modeling of renewable energy systems. 

To run the generation, simply run the following command in your terminal:

```console
reV generation -c config_generation.json
```

To explore more command options, use the `--help` flag, or check on the [reV generation help doc](https://nrel.github.io/reV/_cli/reV%20generation.html) for further documentations: 

```console
reV generation --help
```
