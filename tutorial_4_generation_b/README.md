reV multi-year
===

After running the `generation` module, we now show an example config that take the generated HDF5 files in the `generation` step, then average the multiple-year outputs into a single HDF5 file. Before running the command, we need to first make some changes to source entries in the config file `config_multi-year.json` to point to the correct locations of HDF5 files generated at the previous `generation` step: 

1) The first option is to specify `source_files` to an explicit list of source files. In our case, we need to include the generated HDF5 files for year 2012 and 2013: 

    ```json
    "groups": {
      "none": {
        "source_files": [
          "../tutorial_4_generation_a/tutorial_4_generation_a_generation_2012.h5", 
          "../tutorial_4_generation_a/tutorial_4_generation_a_generation_2013.h5"
        ],
      }
    }
    ```
       
2) The second option is to remove `source_files` entry then specify both `source_dir` (directory to extract source files from) AND `source_prefix` (File prefix to search for in source directory). Note that these two entries must be paired: 

    ```json
    "groups": {
      "none": {
        "source_dir": "../tutorial_4_generation_a/", 
        "source_prefix": "tutorial_4_generation",
      }
    }
    ```

Other config entries that are not covered in previous tutorials are described below. Check on the [reV multi-year help doc](https://nrel.github.io/reV/_cli/reV%20multi-year.html) for further documentations on each: 
- `groups`: The group names will be used as the HDF5 file group name under which the collected data will be stored. You can have exactly one group with the name `"none"` for a “no group” collection (this is typically what you want and all you need to specify).
    - `dsets`: List of datasets to collect. Specifically, we used 
      - "cf_mean": mean capacity factor (fractional).
      - "cf_profile": hourly capacity factor (fractional) profile in local timezone.
      - "lcoe_fcr": the Levelized Cost of Electricity (LCOE) using the fixed-charge-rate method.
      - "ghi_mean": mean global horizontal irradiance (GHI) over a specified time period. GHI can be calculated from Direct Normal Irradiance (DNI) and Diffuse Horizontal Irradiance (DHI).
    - `pass_through_dsets`: Optional list of datasets that are identical in the multi-year files (e.g. input datasets that don’t vary from year to year) that should be copied to the output multi-year file once without a year suffix or means/stdev calculation. In our case, we passed through the SAM config entries that could be found in `config_SAM.json`. 

To see further descriptions of these parameters, please check the help doc [PvWattsv8](https://nrel.github.io/reV/_autosummary/reV.SAM.generation.PvWattsv8.html#reV.SAM.generation.PvWattsv8) from the reV-to-SAM generation interface module. 

After changing the entries for the config file, run the command below to run the multi-year step: 

```console
reV multi-year -c config_multi-year.json
```
