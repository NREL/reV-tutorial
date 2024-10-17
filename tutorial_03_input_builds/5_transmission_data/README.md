Transmission data (Under Construction)
===
The supply curve algorithm uses four types of electricity infrastructure features: transmission
lines, substations, load centers (typically represented by cities), and synthetic features that can be
defined by the user or based on the specific modeling application. Each type of transmission
feature has an associated cost of development based on distance to the feature (this is a static 
$/km cost) and the specific connection costs (e.g., tie-in or substation costs). 

A transmission table is a lookup table with costs and distances associated with all available connections for a reV-supply-curve-aggregation table.
The table will be access in the configuration file from the [tutorial_07_supply-curve](../../tutorial_07_supply-curve/config_supply-curve.json), 
in the `trans_table` entry. 


For further information, please see `reVX` tutorials on [least cost transmission paths building](https://github.com/NREL/reVX/tree/main/reVX/least_cost_xmission). 


Things to do
===
- Here, we just want to describe what the transmission data looks like
  - i.e., its a lookup table with costs and distances associated with all available connections for a reV-supply-curve-aggregation table.
- Describe the different options
  - i.e., straighline and least-cost path (with links to reV/reVX where appropriate)
- Point to Paul's tutorials (done.)
