# reV-tutorial
A tutorial for the Renewable Energy Technical Potenital Model ([reV](https://github.com/NREL/reV)).

This is a draft repository for learning to run reV, both through the command with CLIs and via the Python modules. It contains the sample input data found in the reV repository and sample run directories set up to create outputs for a study area in Rhode Island. Detailed instructions, example runs, and tests can be found in the official reV repository. This repository will supplement that material with a set of python scripts and preconfigured run folders specifically tailored for learning the basics of retrieving/generating the input datasets, configuring the settings, running the model, and troubleshooting common problems. The sample runs will point to the inputs automatically with the hope that it will help the user better understand the required formats needed for building custom inputs. This repo will also include a FAQ page that will be added to as questions arise along with a common gotcha page for common mistakes.

# Brief Description of the reV modeling pipeline

reV is split into three main components: 
1) simulating renewable energy generation and cost potential across a landscape 
2) simulating discrete generation plants with spatial constraints
3) connecting plants to a transmission grid

At its foundation (item 1) reV serves a spatial coordinator for the [Systems Advisor Model](https://sam.nrel.gov/). It runs any number of simulated generators at any number of points for which resource data is availabe. The resource datasets most typically used with reV (at least thus far) include the [National Solar Radiation Database](https://nsrdb.nrel.gov/) (NSRDB) and the [Wind Integration National Dataset Toolkit](https://www.nrel.gov/grid/wind-toolkit.html) (WTK), however any resource dataset can be used if it is formatted correctly.

reV is designed as a set of Python modules, each of which take as inputs the outputs of previous modules. The basic work flow is to take input "resource" datasets, a specifically formatted gridded timeseries of wind or solar irradiance, pass them through module generators (**in reV-Generation**) (wind turbines or photovoltaic panels) to create gridded timeseries of energy outputs and production costs, pass that into an aggregation module (**reV-Supply-Curve-Aggregation**) which combines the resource scale generation values into model plants with plant-level costs and energy production, and finally pass that into a transmission module (**reV-Supply-Curve**) which connects these plants to transmission and updates costs: 


 <h5 align="center"> Resource :arrow_right: Generation :arrow_right: Aggregation :arrow_right: Transmission :arrow_right: Energy and Costs </h5>

 
Land use constraints can be added into the aggregation step to exclude development in parts of the study area, resulting in a range of plant sizes. It is also possible to create time series of plant-level power generation, or "representative profiles" as the final step, resulting in a modeling pipeline that looks like this:

  <h5 align="center"> Resource :arrow_right: Generation :arrow_right: Exclusions :arrow_right: Aggregation :arrow_right: Transmission :arrow_right: Energy and Costs :arrow_right: Representative Profiles </h5>

# Repository Structure
- `data/`: Directory where input datasets are stored.
- `tutorial_#`: Follow the folder sequence to learn about reV CLI workflow. 
