reV multi-year
===========================

After running the `generation` module, we now show an example config that take the generated HDF5 files in the `generation` step, then average the multiple-year outputs into a single HDF5 file. To run the pipeline, simply run the command below: 

1) `source_files`: If this entry is "PIPELINE", the source_files input is determined from the status file of the previous pipeline step. 

```
reV pipeline -c config_pipeline.json
```
