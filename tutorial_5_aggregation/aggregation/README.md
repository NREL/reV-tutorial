Aggregation Pipeline Run
=================

This set of configs will take outputs built in `generation`, apply exclusions,
aggregate to represent plant-scale model points, attach these model plants to a 
transmission grid with tie-lines, and then apply the same aggregation and 
exclusion step to the generation profiles. Once the configs are setup, 
the command to run all of this is the same as in generation:

```
reV pipeline -c config_pipeline.json --monitor
```


Production Notes:
 - These runs depend on two very specific input formats: the exclusion HDF5 file
  and the transmission connection table.
 - More details about supply curve aggregation/aggregation steps can be found at:
    https://nrel.github.io/reV/_cli/reV%20supply-curve-aggregation.html

Additional Notes:
    Solar:
        - It is important to include (in most cases) a minimum contiguous area 
        filter or area filter kernen when running solar reV runs. This accounts
         for the need for solar panels to be near each other unlike wind power 
         which can be dispersed.  
        - Minimum area (in km2) required to keep an isolated cluster of 
        (included) land within the resulting exclusions mask.
         Any clusters of land with areas less than this value will be marked as exclusions. 
        - Resolution for solar runs should be lower than wind runs
        - Power density is much higher when compared with wind

