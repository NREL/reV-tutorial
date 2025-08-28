# reV-tutorial
A tutorial for the Renewable Energy Technical Potenital Model ([reV](https://github.com/NREL/reV)).

This is a repository for learning to run reV, both through Commands-Line Interface (CLIs) and via the Python modules. It contains the sample input data found in the reV repository and sample run directories set up to create outputs for a study area in Rhode Island. Detailed instructions, example runs, and tests can be found in the official reV repository. This repository will supplement that material with a set of python scripts and preconfigured run folders specifically tailored for learning the basics of retrieving/generating the input datasets, configuring the settings, running the model, and troubleshooting common problems. The sample runs will point to the inputs automatically with the hope that it will help the user better understand the required formats needed for building custom inputs. This repo will also include a FAQ page that will be added to as questions arise along with a common gotcha page for common mistakes.

# Brief description of the reV modeling pipeline

reV is split into three main components: 
1) simulating renewable energy generation and cost potential across a landscape 
2) simulating discrete generation plants with spatial constraints
3) connecting plants to a transmission grid

At its foundation (item 1) reV serves a spatial coordinator for the [Systems Advisor Model](https://sam.nrel.gov/). It runs any number of simulated generators at any number of points for which resource data is availabe. The resource datasets most typically used with reV (at least thus far) include the [National Solar Radiation Database](https://nsrdb.nrel.gov/) (NSRDB) and the [Wind Integration National Dataset Toolkit](https://www.nrel.gov/grid/wind-toolkit.html) (WTK), however any resource dataset can be used if it is formatted correctly.

reV is designed as a set of Python modules, each of which take as inputs the outputs of previous modules. The basic work flow is to take input "resource" datasets, a specifically formatted gridded timeseries of wind or solar irradiance, pass them through module generators (**in reV-Generation**) (wind turbines or photovoltaic panels) to create gridded timeseries of energy outputs and production costs, pass that into an aggregation module (**reV-Supply-Curve-Aggregation**) which combines the resource scale generation values into model plants with plant-level costs and energy production, and finally pass that into a transmission module (**reV-Supply-Curve**) which connects these plants to transmission and updates costs: 


 <h5 align="center"> Resource :arrow_right: Generation :arrow_right: Aggregation :arrow_right: Transmission :arrow_right: Energy and Costs </h5>

 
Land use constraints can be added into the aggregation step to exclude development in parts of the study area, resulting in a range of plant sizes. It is also possible to create time series of plant-level power generation, or "representative profiles" as the final step, resulting in a modeling pipeline that looks like this:

  <h5 align="center"> Resource :arrow_right: Generation :arrow_right: Exclusions :arrow_right: Aggregation :arrow_right: Transmission :arrow_right: Energy and Costs :arrow_right: Representative Profiles </h5>


# Tutorials on reV CLI methods

The quickest and easiest way to get started with reV is to use the **JSON-CLI** workflow. This involves building a json configuration file for a module you want to run and running that module with the corresponding CLI command. You can also configure several modules in an input-output pipeline and run each with a single command. The configurations will tell reV which SAM generator configurations to run and where, what variables to generate, which land-use assumptions to use, etc. It will also tell reV how to work with your system to most efficiently build these outputs (e.g. how to split the work across CPUs, how to split work across nodes for distributed systems, what memory utilization limits to use, etc.). This method is convenient in that you don't need to edit any Python scripts, is relatively straightforward to set up and run directly from your terminal, and leaves a tidy way to keep track of run parameters when recreating or reviewing a reV run. 

To learn details about the reV JSON-CLI workflow, go into each `tutorial_#_module` sequentially and follow the instruction in each. Go to `data` folder to examine input datasets used for the commands used in the tutorials.

# reV Documentation
Use this documentation in tandem with the tutorial series: https://nrel.github.io/reV/_cli/cli.html

# Getting started with the tutorial
Tutorial #1 (`tutorial_1_concepts`) will introduce key concepts (particularly that of "technical potential") needed to understand what the outputs of the reV model represent. It is recommended to start here, but if you understand all that and wish to get on with running the model, you may skip this one. Each subsequent tutorial folder contains reV configuration files and a README describing how to use them to run reV and generate outputs. The READMEs will also describe what each configuration parameter means. These tutorials are ordered by increasing complexity. Early tutorials should be setup such that you may simply run the model without editing configuration files, though later tutorials will require user input in order to work.
