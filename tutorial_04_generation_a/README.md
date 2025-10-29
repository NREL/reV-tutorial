reV generation
===========================

This tutorial focuses on the **generation** module of the NREL reV model. When running reV, a series of JSON files are used to inform the model of what configuration files you want to use and where you want to use them. Throughout the config there are parameters that are required and ones that are optiona. We'll be focusing on the required parameters here, later tutorials will introduce more options. This tutorial includes a sample **configuration JSON** file (`config_generation.json`) that specify the simulation parameters, including system specifications, time periods, output requests, etc. This example module runs at several points in Rhode Island for 2012 and 2013 NSRDB data.

The `config_generation.json` entries that correspond to the input data created in `tutorial_3_input_builds/` are described below: 

1) `technology`: A string representing the SAM module you wish to run.
    - Not all SAM generation modules are available. Available modules include "pvwattsv5", "pvwattsv7", "pvwattsv8", "Pvsamv1", "tcsmolten_salt", "solarwaterheat", "lineardirectsteam", "geothermal", "windpower", and "mhkwave".
2) `sam_files`: The key and location of your System Advisor Model (SAM) configuration file (or files). 
    - A set of key-value pairs which correspond to the "config" column in the project points file and the path to the SAM configuration file associated with it.
3) `project_points`: The path to a project points file. 
    - This input specifies the geographical locations (lat/lon) where the generation module will be performed. This file may also contain spatially-explicit SAM parameters by providing a new column named after the target SAM parameter.
4) `resource_file`: One or multiple paths to your resource HDF5 file(s) corresponding with the chosen technology module.
    - This input may be a single string for a single resource file, a list that contains the full path to multiple resource files, or a single string with a set of brackets (`{}`) that will be filled in by the `analysis_years` entry to represent multiple resource years (in this case, year 2012 and 2013).
5) `output_request`: A list of strings representing the datasets you want in the output HDF5 file.
    - This will include parameters derived from both the selected SAM generation module and the SAM economics model. For a complete list of all available outputs, see the Outputs Group for your SAM module in the PySAM docs. For available generation outputs in this example look [here](https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#outputs-group) and for the one economic output in this example look [here](https://nrel-pysam.readthedocs.io/en/latest/modules/Lcoefcr.html#outputs-group). Note that the availability of these outputs will depend on the information provided in the SAM config you use. 
    - Also note that most available outputs may be identified using the SAM variable names directly, but some of the more common outputs requested in reV have names specific to reV. For example, the `capacity_factor` SAM variable (description [here](https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.Outputs.capacity_factor)) is represented as `cf_mean` in reV. The full capacity factor time series in reV is called `cf_profile` while this variable isn't explicitly defined in SAM.
    - Special note: for solar modules, `cf_mean` and `cf_profile` in reV, or `capacity_factor` in reV and SAM, all represent generation in alternating current (AC) over capacity in direct current (DC). If you want AC generation over AC capacity, use `cf_mean_ac` or `capacity_factor_ac` for average capacity factors and `cf_profile_ac` for the time series. See reV's definition of these variables in the code base starting [here](https://github.com/NREL/reV/blob/0f71e9e97cc320a085c519819750f3a5a6889f5f/reV/SAM/generation.py#L1103).
    - Below is a basic output request with documentation links for each variable in the reV documentation:
    
    <pre>
    "output_request": [
      "cf_mean", <a href="https://nrel.github.io/reV/_autosummary/reV.SAM.generation.PvWattsv8.html#reV.SAM.generation.PvWattsv8.cf_mean"># Description</a>
      "cf_profile", <a href="https://nrel.github.io/reV/_autosummary/reV.SAM.generation.PvWattsv8.html#reV.SAM.generation.PvWattsv8.cf_profile"># Description</a>
      "lcoe_fcr", <a href="https://nrel.github.io/reV/_autosummary/reV.SAM.econ.LCOE.html#reV.SAM.econ.LCOE.lcoe_fcr"># Description</a>
      "ghi_mean", <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.Outputs.gh"># Description</a>
      "gh", <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.Outputs.gh"># Description</a>
    ]</pre>

Other parameters control your system usage and logging behavior:

6) `log_directory`: Path to directory where logs should be written. Path can be relative and does not have to exist on disk (it will be created if missing). In our case, we created the logs at the current directory: `"./logs/"`. Each log file will be named after the process ID of the job. Information logging and uncaught errors will be writted to a file with the `.o` extension. Warnings and errors will be logged to a separate `.e` file.
7) `execution_control`: Dictionary containing execution control arguments. 
8) `log_level`: String representation of desired logger verbosity. Suitable options are "DEBUG" (most verbose) and "INFO" (moderately verbose). 

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
