Transmission data (Under Construction)
===
A transmission table is a lookup table with costs and distances associated with all available connections for a `reV` supply-curve-aggregation table.
The table is located in [data/](../../data/transmission/) folder and will be access in the configuration file from the [tutorial_07_supply-curve](../../tutorial_07_supply-curve/config_supply-curve.json), in the `trans_table` entry. 

The supply curve algorithm uses four types of electricity infrastructure features: transmission lines, substations, load centers (typically represented by cities) and synthetic features that can be defined by the user or based on the specific modeling application. Each type of transmission 
feature has an associated cost of development based on distance to the feature (this is a static $/km cost) and the specific connection costs (e.g., tie-in or substation costs). For more information, please see [Maclaurin et al. 2019](https://www.nrel.gov/docs/fy19osti/73067.pdf). This paper used the **straight-line** distance between a prospective site and existing electrical transmission to estimate the cost of a spur line and applied a single cost per MW-mile assumption. [Lopez et al. 2023](https://www.nrel.gov/docs/fy24osti/87843.pdf) introduce a **least-cost-path** methodology that considers the components listed below: 
- Siting constraints
- Regional component costs (hard costs)
- Land composition costs (soft costs)
- Point-of-interconnection (POI) costs
- Network upgrade costs

The `reVX` tutorial on [least cost transmission paths building](https://github.com/NREL/reVX/tree/main/reVX/least_cost_xmission) gives steps to determine least cost transmission paths from land-based and offshore wind and solar farms (supply curve (SC) points) to the electrical grid. 

Things to do
===
- Here, we just want to describe what the transmission data looks like
  - i.e., its a lookup table with costs and distances associated with all available connections for a reV-supply-curve-aggregation table.
- Describe the different options
  - i.e., straighline and least-cost path (with links to reV/reVX where appropriate)
- Point to Paul's tutorials (done.)
