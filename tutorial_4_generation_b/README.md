reV multi-year
===

After running the `generation` module, we now show an example config that take the generated HDF5 files in the `generation` step, then average the multiple-year outputs into a single HDF5 file. Before running the command, we need to first make some changes to source entries in the config file `config_multi-year.json` to point to the correct locations of HDF5 files generated at the previous `generation` step: 

1) The first option is to specify `source_files` to an explicit list of source files. In our case, we need to include the generated HDF5 files for year 2012 and 2013: 

    ```json
        "source_files": [
          "../tutorial_4_generation_a/tutorial_4_generation_a_generation_2012.h5", 
          "../tutorial_4_generation_a/tutorial_4_generation_a_generation_2013.h5"
        ],
    ```
       
2) The second option is to remove `source_files` entry then specify both `source_dir` (directory to extract source files from) AND `source_prefix` (File prefix to search for in source directory). Note that these two entries must be paired: 

    ```json
    "source_dir": "../tutorial_4_generation_a/", 
    "source_prefix": "tutorial_4_generation",
    ```

After changing the sources for the config file, run the command below to run the multi-year step: 

```
reV multi-year -c config_multi-year.json
```
