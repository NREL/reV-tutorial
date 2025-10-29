reV generation
===========================

The reV-generation module controls what and where the System Advisor Model (SAM) runs. In the CLI method, this coordination is controlled using a JSON configuration file. This file has many required and optional parameters, but we'll focus mostly on the required parameters here and introduce more options in later tutorials as they become relevant. This repository folder includes two sample resource files, a sample SAM configuration file, and a sample reV-generation configuration JSON file (`config_generation.json`) that specifies the simulation parameters, including system specifications, time periods, output requests, etc. This example module is setup to run a subset of points in Rhode Island for 2012 and 2013 in the National Solar Radiation Data Base (NSRDB). For a complete list of options, use the `--help` flag, or check the [reV generation page](https://nrel.github.io/reV/_cli/reV%20generation.html) for further documentation: 

```bash
reV generation --help
```
## Configuration Parameters
For a basic run, these following entries in `config_generation.json` are the most important to understand: 

1) `technology`: A string representing the SAM module you wish to run.
    - Not all SAM generation modules are available in reV. Available modules include "pvwattsv5", "pvwattsv7", "pvwattsv8", "Pvsamv1", "tcsmolten_salt", "solarwaterheat", "lineardirectsteam", "geothermal", "windpower", and "mhkwave".
2) `project_points`: The path to your project points file. 
    - This input is a CSV table that specifies the geographical locations where the generation module will be run. These locations are represented as the index positions of the resource data in a "gid" field. This file may also contain spatially-explicit SAM parameters by providing a new column named after the target SAM parameter.
3) `sam_files`: A dictionary containing paths to your SAM configuration file (or files). 
    - This is a set of key-value pairs which correspond to the "config" column in your project points file. reV will use the "config" value with this dictionary to determine which SAM configurations to use for each location in your study area.
4) `resource_file`: One or multiple paths to your resource HDF5 data 
    - This input may be a single string for a single resource file path, a list that contains paths for multiple resource files, or a single string with a set of brackets (`{}`) that will be filled in by the `analysis_years` entry and which will represent multiple resource years (in this case, year 2012 and 2013).
5) `output_request`: A list of strings representing the datasets you want in the output HDF5 file.
    - This will include parameters derived from the selected SAM generation and economic modules. For a complete list of all available outputs, see the Outputs Group for your SAM module in the PySAM docs. For available generation outputs in this example look [here](https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#outputs-group) and for the one economic output in this example look [here](https://nrel-pysam.readthedocs.io/en/latest/modules/Lcoefcr.html#outputs-group). Note that the availability of these outputs will depend on the information provided in the SAM config you use. 
    - Also note that most available outputs may be identified using the SAM variable names directly, but some of the more common outputs requested in reV have names specific to reV. For example, the `capacity_factor` SAM variable (description [here](https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.Outputs.capacity_factor)) is represented as `cf_mean` in reV. The full capacity factor time series in reV is called `cf_profile` while this variable isn't explicitly defined in SAM.
    - Special note: for solar modules, `cf_mean` and `cf_profile` in reV, or `capacity_factor` in reV and SAM, all represent generation in alternating current (AC) over capacity in direct current (DC). If you want AC generation over AC capacity, use `cf_mean_ac` or `capacity_factor_ac` for average capacity factors and `cf_profile_ac` for the time series. See reV's definition of these variables in the code base starting [here](https://github.com/NREL/reV/blob/0f71e9e97cc320a085c519819750f3a5a6889f5f/reV/SAM/generation.py#L1103).
    - Below is the sample output request with links to descriptions or comments for each variable:
    
        <pre>
        "output_request": [
            "cf_mean",  # reV-derived, see <a href="https://nrel.github.io/reV/_autosummary/reV.SAM.generation.PvWattsv8.html#reV.SAM.generation.PvWattsv8.cf_mean">description</a>
            "cf_profile",  # reV-derived, see <a href="https://nrel.github.io/reV/_autosummary/reV.SAM.generation.PvWattsv8.html#reV.SAM.generation.PvWattsv8.cf_profile">description</a>
            "lcoe_fcr",  # reV-derived, see <a href="https://nrel.github.io/reV/_autosummary/reV.SAM.econ.LCOE.html#reV.SAM.econ.LCOE.lcoe_fcr">description</a>
            "gh",  # Directly from SAM, see <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.Outputs.gh">description</a>
            "ghi_mean",  # reV-derived, see <a href="https://github.com/NREL/reV/blob/0f71e9e97cc320a085c519819750f3a5a6889f5f/reV/SAM/generation.py#L161">method</a>
            "capital_cost"  # Passed through from SAM inputs, see <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.Outputs.gh">description</a>
        ]</pre>

Other parameters control your system usage and logging behavior:

6) `execution_control`: Dictionary containing execution control arguments.
- This can be left out entirely for small, local runs, but we left in a few to introduce this entry:
    - `max_workers`: The number of CPU cores to split work across. This defaults to 1 for serial compute.
    - `sites_per_worker`: The number of sites (i.e., project points) to process at a time on each CPU core.
    - `memory_utilization_limit`: A target maximum memory use percentage before reV starts dumping data from memory to disk.

7) `log_directory`: Path to directory where logs should be written.
-  This path can be relative and does not have to exist on disk (it will be created if missing). In our case, we created the logs at the current directory: `"./logs"`. Each log file will be named after containing folder, the module being run, and the process ID of the job. Information logging and uncaught errors will be writted to a file with the `.o` extension. Warnings and raised exceptions will be logged to a separate `.e` file.
8) `log_level`: String representation of desired logger verbosity. Suitable options are "DEBUG" (most verbose) and "INFO" (moderately verbose). 

## Running the Model
Once the configuration file is filled, run the model by simply calling the following command in your terminal:

```console
reV generation -c config_generation.json
```

Here, the base command is `reV`, the submodule is `generation`, the `-c` option stands for "config" and it receives the path to the reV-generation configuration file. You will see various logging information printed to your console. This will include version information about reV and its dependencies, validations of your configuration parameters, and indications of steps the model is taking. Once the model is finished (it should be quick), you will hopefully see a completion statement with the location of the output file and a final statement stating: `Completed job 'tutorial_04_generation_a_generation_j1`, indicating that the job is finished.

If you receive an error instead, this may indicate an mistake in your configuration file. If everything looks good on that front, try examining the files in your `logs` directory for clues about what went wrong.

## Checking Outputs
Even if you received no obvious errors, it is always a good idea to check the logs for warnings or buried excpetions and that the output values make sense. Valid ranges of values will depend on the model you are running, but there are some easy characteristics to check for in every case. There are several ways to examine the values in your output file. Since `reV` uses the reV Exchange model (`rex`) to handle HDF5 files, we will go ahead and introduce a useful class from that package here.

In a Python session, import the `Resource` class from `rex` and use it to open your files. Here is an example for the first output file:

```python
from rex import Resource
gen = Resource("./tutorial_04_generation_a_generation_2012.h5")
```

Now you have created a pointer to the data in the output HDF5 file, but have not pulled any data in yet. Let's pull that data into memory (the outputs will be Numpy arrays) and take a look at the average capacity factor dataset to make sure we get reasonable values. A first good check is that you got values. If you got all zeros everywhere for a whole year, that's an excellent clue that something probably went wrong and you should check your logs for exceptions. 

```python
cf_mean = gen["cf_mean"]
print(any(cf_mean == 0))
# False
```

So, this indicates that every site in our sample was generating at least something.

The next check is if the output values are within an expected range. You might not know what that minimum or maximum value should be for other technologies, so that will require some research. However, without any knowledge about solar capacity factors, we already know that PV systems aren't generating anything at night (50% of our generation is lost there) and for about half of the day the sun is either rising or falling, so we are generating less than full capacity during most of the day. On top of this, clouds, snow, dust, and other system losses will pull more generation away from the potential energy hitting the solar panels. Tracking, bifacility, high DC/AC ratios, and other technologcial advancements can gain some of this energy back, but only so much is possible. For a solar run, the most advanced technology in the most ideal locations (of which Rhode Island is certainly not one) for a properly configured SAM model will rarely have an average capacity factor value over .30, so we expect significantly lower average values for this run. 

Anyways, let's pull out that value and check for obviously wrong values.

```python
print(f"Min value: {cf_mean.min()}")
# Min value: 0.1708141267299652

print(f"Mean value: {cf_mean.mean()}")
# Mean value: 0.1791270226240158

print(f"Max value: {cf_mean.max()}")
# Max value: 0.18519368767738342
```

So, these values don't look too bad, they are probably higher than what currently exists in Rhode Island but are low enough to be believable.

Did you get unreasonable values instead? If so, were they absurdly high or absurdly low? That could indicate either a configuration or a runtime error, check the logs for errors and make sure your SAM parameters are correct. If no errors are found in either of those, perhaps your resource file has some errors. There is no end to the list of possible errors, but we can only do our best, so keep looking and you'll probably find one eventually.

Are they only uncomfortably high or unreasonably low, but relatively close to what you'd expect? That sounds more like a simpler configuration error. Check the SAM config for mistakes in your losses, DC/AC ratio, inverter efficiency, or other parameters that might affect generation efficiency. It could still be anything, of course.

What about instantaneous generation. We know that a capacity factor should never go above one, so that's an easy check. Let's pull out the time series and see if that's true:

```python
cf_profile = gen["cf_profile"]
print((cf_profile > 1).any())
# False
```

Of course, you'll want follow a similar process any other output you requested. Once you've checked everything for clearly wrong or suspicious values, you have completed the generation step and can move on to the next tutorial ([`tutorial_04_generation_b`](https://github.com/NREL/reV-tutorial/tree/master/tutorial_04_generation_b)), where we'll look at combining multiple yearly files into one.
