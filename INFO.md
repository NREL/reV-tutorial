
reV allows researchers to include exhaustive spatial representation of the built and natural environment into the generation and cost estimates that it computes.
reV allows the user to model a technology from a single site up to an entire continent at temporal resolutions ranging from five minutes to hourly, spanning a single year or multiple decades

Further documenation can be found at:
https://www.nrel.gov/docs/fy19osti/73067.pdf

A general reV pipeline consists of:

1. Generation:
    - reV generation analysis runs SAM simulations by piping in renewable energy resource data (usually from the NSRDB or WTK), loading the SAM config, and then executing the PySAM compute module for a given technology.

2. Supply Curve Aggregation
    - reV supply curve aggregation combines a high-resolution (e.g. 90m) exclusion dataset with a (typically) lower resolution (e.g. 2km) generation dataset by mapping all data onto the high- resolution grid and aggregating it by a large factor (e.g. 64 or 128). The result is coarsely-gridded data that summarizes capacity and generation potential as well as associated economics under a particular land access scenario. This module can also summarize extra data layers during the aggregation process, allowing for complementary land characterization analysis.

3. Supply Curve
    - reV supply curve computes the transmission costs associated with each supply curve point output by reV supply curve aggregation. Transmission costs can either be computed competitively (where total capacity remaining on the transmission grid is tracked and updated after each new connection) or non-competitively (where the cheapest connections for each supply curve point are allowed regardless of the remaining transmission grid capacity). In both cases, the permutation of transmission costs between supply curve points and transmission grid features should be computed using the reVX Least Cost Transmission Paths utility.

4. Rep Profiles
    - reV rep profiles compute representative generation profiles for each supply curve point output by reV supply curve aggregation. Representative profiles can either be a spatial aggregation of generation profiles or actual generation profiles that most closely resemble an aggregated profile (selected based on an error metric)

Other included steps:
1. Collect
    - Collect data generated across multiple nodes into a single HDF5 file.

2. Econ
    - reV econ analysis runs SAM econ calculations, typically to compute LCOE (using PySAM.Lcoefcr.Lcoefcr), though PySAM.Singleowner.Singleowner or PySAM.Windbos.Windbos calculations can also be performed simply by requesting outputs from those computation modules. See the keys of Econ.OPTIONS for all available econ outputs. Econ computations rely on an input a generation (i.e. capacity factor) profile. You can request reV to run the analysis for one or more “sites”, which correspond to the meta indices in the generation data.

3. Multi-Year
    - reV multi-year combines reV generation data from multiple years (typically stored in separate files) into a single multi-year file. Each dataset in the multi-year file is labeled with the corresponding years, and multi-year averages of the yearly datasets are also computed.



Useful cli commands
1. reV template configs:

    https://nrel.github.io/reV/_cli/reV%20template-configs.html
    This will generate tempaltes of all the configs needed. 
    An example of these files can be found in the folder example_configs