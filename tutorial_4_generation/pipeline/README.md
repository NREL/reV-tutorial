An Example Pipeline Run
===========================

After running the `generation` module, we now show an example set of configs that take the generated HDF5 files in the `generation` step, then average the multiple-year outputs into a single HDF5 file. To run the pipeline, simply run the command below: 

```
reV pipeline -c config_pipeline.json --monitor
```
