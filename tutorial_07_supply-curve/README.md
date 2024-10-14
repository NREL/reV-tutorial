reV supply-curve
=================

`reV supply-curve` module computes the transmission interconnection costs associated with each supply curve point output by reV supply curve aggregation. Transmission costs can either be computed competitively (where total capacity remaining on the transmission grid is tracked and updated after each new connection) or non-competitively (where the cheapest connections for each supply curve point are allowed regardless of the remaining transmission grid capacity). In both cases, the permutation of transmission costs between supply curve points and transmission grid features should be computed using the [reVX Least Cost Transmission Paths](https://github.com/NREL/reVX/tree/main/reVX/least_cost_xmission) utility. 

Descriptions to the config entries of the reV supply-curve in `config_supply-curve.json` are listed below, following the entry order in the JSON: 

- `sc_points`: Path to CSV or JSON or DataFrame containing supply curve point summary. Can also be a filepath to a reV bespoke HDF5 output file where the meta dataset has the same format as the supply curve aggregation output. If executing reV from the command line, this input can also be `"PIPELINE"` to parse the output of the previous pipeline step and use it as input to this call. However, note that duplicate executions of any preceding commands within the pipeline may invalidate this parsing, meaning the sc_points input will have to be specified manually.
- `simple`: Option to run the simple sort (does not keep track of capacity available on the existing transmission grid). If `False`, a full transmission sort (where connections are limited based on available transmission capacity) is run. Note that the full transmission sort requires the `avail_cap_frac` and `line_limited` inputs. By default, `True`.
- `trans_table`: Path to CSV or JSON or DataFrame containing supply curve transmission mapping. This can also be a list of transmission tables with different line voltage (capacity) ratings. See the [reVX Least Cost Transmission Paths](https://github.com/NREL/reVX/tree/main/reVX/least_cost_xmission) utility to generate these input tables.
- `transmission_costs`: Dictionary of transmission feature costs or path to JSON file containing a dictionary of transmission feature costs. These costs are used to compute transmission capital cost if the input transmission tables do not have a "trans_cap_cost" column (this input is ignored otherwise). The dictionary must include:
    - "center_tie_in_cost": Cost of connecting to a load center in $/MW.
    - "line_cost": Cost of building transmission line during connection in $/MW-km.
    - "line_tie_in_cost": Cost of connecting to a transmission line in $/MW
    - "sink_tie_in_cost": Cost of connecting to a synthetic load center (infinite sink) in $/MW. 
    - "station_tie_in_cost": Cost of connecting to a substation in $/MW. 

To run reV supply-curve module after configured: 
```
reV supply-curve -c config_supply-curve.json
```
