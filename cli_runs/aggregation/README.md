Aggregation Pipeline Run
=================

This set of configs will take outputs built in `generation`, apply exclusions, aggregate to represent plant-scale model points, attach these model plants to a transmission grid with tie-lines, and then apply the same aggregation and exclusion step to the generation profiles. Once the configs are setup, the command to run all of this is the same as in generation:

```
reV -c config_pipeline.json pipeline --monitor
```


Production Notes:
 - These runs depend on two very specific input formats: the exclusion HDF5 file and the transmission connection table.
 - Tutorials on how to build these inputs will be available soon.
