reV aggregation
===
reV supply curve aggregation combines a high-resolution (e.g. 90m) exclusion dataset with a (typically) lower resolution (e.g. 2km) generation dataset by mapping all data onto the high- resolution grid and aggregating it by a large factor (e.g. 64 or 128). The result is coarsely-gridded data that summarizes capacity and generation potential as well as associated economics under a particular land access scenario. This module can also summarize extra data layers during the aggregation process, allowing for complementary land characterization analysis.

Descriptions to the config entries of the reV aggregation in `config_aggregation.json` are listed below, following the entry order in the JSON: 
- `cf_dset`: Dataset name from the reV generation HDF5 output file containing a 1D dataset of mean capacity factor values. This dataset will be mapped onto the high-resolution grid and used to compute the mean capacity factor for non-excluded area. By default, `"cf_mean-means"`.
- `data_layers`: Dictionary of aggregation data layers of the format below:
    ```json
    "data_layers": {
        "output_layer_name": {
            "dset": "layer_name",
            "method": "mean",
            "fpath": "/path/to/data.h5"
        },
        "another_output_layer_name": {
            "dset": "input_layer_name",
            "method": "mode",
            "optional 'fpath' key omitted"
        },
    }
    ```
- `log_directory`: Same as previous tutorials, the path to directory where logs should be written. By default, `"./logs"`.
- `excl_dict`: Dictionary of exclusion keyword arguments of the format `{layer_dset_name: {kwarg: value}}`, where `layer_dset_name` is a dataset in the exclusion h5 file and the `kwarg: value` pair is a keyword argument to the [reV.supply_curve.exclusions.LayerMask](https://nrel.github.io/reV/_autosummary/reV.supply_curve.exclusions.LayerMask.html#reV.supply_curve.exclusions.LayerMask) class. Note that all the keys given in this dictionary should be datasets of the `excl_fpath` file. If `None` or empty dictionary, no exclusions are applied. By default, `None`.
- `excl_fpath`: Filepath to exclusions data HDF5 file. The exclusions HDF5 file should contain the layers specified in excl_dict and data_layers. These layers may also be spread out across multiple HDF5 files, in which case this input should be a list or tuple of filepaths pointing to the files containing the layers. Note that each data layer must be uniquely defined (i.e.only appear once and in a single input file).
- `gen_fpath`: Filepath to HDF5 file with `reV generation` output results. If `None`, a simple aggregation without any generation, resource, or cost data is performed. Since we are executing reV from the command line in this tutorial, this input can be set to `"PIPELINE"` to parse the output from one of these preceding pipeline steps: multi-year (see [tutorial_4_generation_b](../tutorial_4_generation_b/README.md)), collect, or econ.
- `lcoe_dset`: Dataset name from the reV generation HDF5 output file containing a 1D dataset of mean LCOE values. This dataset will be mapped onto the high-resolution grid and used to compute the mean LCOE for non-excluded area, but only if the LCOE is not re-computed during processing (see the `recalc_lcoe` input below for more info). By default, `"lcoe_fcr-means"`.
- `recalc_lcoe`: Flag to re-calculate the LCOE from the multi-year mean capacity factor and annual energy production data. This requires several datasets to be aggregated in the h5_dsets input:
    - system_capacity
    - fixed_charge_rate
    - capital_cost
    - fixed_operating_cost
    - variable_operating_cost
    
    If any of these datasets are missing from the reV generation HDF5 output, or if recalc_lcoe is set to False, the mean LCOE will be computed from the data stored under the `lcoe_dset` instead. By default, `True`.
- `power_density`: Power density value (in MW/km2).
- `res_class_bins`: Optional input to perform separate aggregations for various resource data ranges. If `None`, only a single aggregation per supply curve point is performed. Otherwise, this input should be a list of floats or ints representing the resource bin boundaries. One aggregation per resource value range is computed, and only pixels within the given resource range are aggregated. By default, `None`.
- `resolution`: Supply Curve resolution. This value defines how many pixels are in a single side of a supply curve cell. For example, a value of 64 would generate a supply curve where the side of each supply curve cell is 64x64 exclusion pixels. By default, 64.
- `tm_dset`: Dataset name in the excl_fpath file containing the techmap (exclusions-to-resource mapping data). This data layer links the supply curve GID’s to the generation GID’s that are used to evaluate performance metrics such as mean_cf. If executing reV from the command line, you can specify a name that is not in the exclusions HDF5 file (`techmap_nsrdb_ri_truth`), and reV will calculate the techmap for you. Note however that computing the techmap and writing it to the exclusion HDF5 file is a blocking operation, so you may only run a single reV aggregation step at a time this way.
- `h5_dsets`: Optional list of additional datasets from the `reV generation/econ` HDF5 output file to aggregate. If `None`, no extra datasets are aggregated.


For further information, please check the reV supply-curve-aggregation [help doc](https://nrel.github.io/reV/_cli/reV%20supply-curve-aggregation.html). After configuring, run the reV supply-curve-aggregation module at your terminal: 
```
reV supply-curve-aggregation -c config_aggregation.json
```
