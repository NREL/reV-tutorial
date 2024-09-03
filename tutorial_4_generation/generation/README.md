Simple Generation Run
===========================

This is a simple set of configs that take a photovoltaic SAM module or a Wind SAM module, run it at several points in Rhode Island for 2012 and 2013 NSRDB data, then average the outputs into a single HDF5 file. To run, simply navigate to `solar` folder and use the following command in your terminal:

```
reV pipeline -c config_pipeline.json --monitor
```
More On SAM:
Further reading can be done on the specifics of the SAM configs.

    - Solar: https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html
        
    - Wind: https://nrel-pysam.readthedocs.io/en/latest/modules/Windpower.html


Production Notes:

The project points file must have two columns, anything else is optional:
  1) "gid": The index position of the x-axis of the resource array, or the row index of the resource meta data table.
  2) "config": The key associated with a SAM config in the config_gen.json file. For solar it is 'default' and wind it is 'onshore'.

The "sam_files" entry in config_gen.json contains a set of key-value pairs which represent the "config" column in the project points file and the SAM configuration associated with it.
