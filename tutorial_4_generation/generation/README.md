Simple Generation Run
===========================
This is a simple set of configs that take a photovoltaic SAM module or a Wind SAM module, run it at several points in Rhode Island for 2012 and 2013 NSRDB data. 
To run, simply run the following command in your terminal:

```
reV generation -c config_gen.json
```

The `config_gen.json` specifies file locations of files that generated from previous tutorials, including:

- **Project points**: It specifies the geographical locations (lat/lon) where the generation module will be performed. 
- **Resource data**: This is typically in HDF5 format that contains solar (NSRDB) or wind (WTK) data. 

To explore more command options, use the `--help` flag: 

```
reV generation --help
```

More On SAM:
Further reading can be done on the specifics of the SAM configs.

- Solar: [https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html](https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html)
        
- Wind: [https://nrel-pysam.readthedocs.io/en/latest/modules/Windpower.html](https://nrel-pysam.readthedocs.io/en/latest/modules/Windpower.html)


Production Notes:

The project points file must have two columns, anything else is optional:
  1) "gid": The index position of the x-axis of the resource array, or the row index of the resource meta data table.
  2) "config": The key associated with a SAM config in the config_gen.json file. For solar it is 'default' and wind it is 'onshore'.

The "sam_files" entry in config_gen.json contains a set of key-value pairs which represent the "config" column in the project points file and the SAM configuration associated with it.
