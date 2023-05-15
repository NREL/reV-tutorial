# reV-tutorial
A tutorial for the Renewable Energy Technical Potenital Model ([reV](https://github.com/NREL/reV)).

This is a draft repository for learning to run reV, both through the command with CLIs and via the Python modules. It contains the sample input data found in the reV repository and sample run directories set up to create outputs for a study area in Rhode Island. Detailed instructions, example runs, and tests can be found in the official reV repository. This repository will supplement that material with a set of python scripts and preconfigured run folders specifically tailored for learning the basics of retrieving/generating the input datasets, configuring the settings, running the model, and troubleshooting common problems. The sample runs will point to the inputs automatically with the hope that it will help the user better understand the required formats needed for building custom inputs. This repo will also include a FAQ page that will be added to as questions arise along with a common gotcha page for common mistakes.

# Brief Description of the reV modeling pipeline

reV is split into three main components: 1) simulating renewable energy generation and cost potential across a landscape, 2) simulating discrete generation plants with spatial constraints, and 3) connecting plants to a transmission grid. At its foundation (item 1) reV serves a spatial coordinator for the [Systems Advisor Model](https://sam.nrel.gov/). It runs any number of simulated generators at any number of points for which resource data is availabe. The resource datasets most typically used with reV (at least thus far) include the [National Solar Radiation Database](https://nsrdb.nrel.gov/) (NSRDB) and the [Wind Integration National Dataset Toolkit](https://www.nrel.gov/grid/wind-toolkit.html) (WTK), however any resource dataset can be used if it is formatted correctly.

reV is designed as a set of Python modules, each of which take as inputs the outputs of previous modules. The basic work flow is to take input "resource" datasets, a specifically formatted gridded timeseries of wind or solar irradiance, pass them through module generators (**in reV-Generation**) (wind turbines or photovoltaic panels) to create gridded timeseries of energy outputs and production costs, pass that into an aggregation module (**reV-Supply-Curve-Aggregation**) which combines the resource scale generation values into model plants with plant-level costs and energy production, and finally pass that into a transmission module (**reV-Supply-Curve**) which connects these plants to transmission and updates costs: 


 <h5 align="center"> Resource :arrow_right: Generation :arrow_right: Aggregation :arrow_right: Transmission :arrow_right: Energy and Costs </h5>

 
Land use constraints can be added into the aggregation step to exclude development in parts of the study area, resulting in a range of plant sizes. It is also possible to create time series of plant-level power generation, or "representative profiles" as the final step, resulting in a modeling pipeline that looks like this:

  <h5 align="center"> Resource :arrow_right: Generation :arrow_right: Exclusions :arrow_right: Aggregation :arrow_right: Transmission :arrow_right: Energy and Costs :arrow_right: Representative Profiles </h5>


# Getting Started - Installating reV

The simplest way to install reV and it's supporting packages ([PySAM](https://github.com/NREL/pysam), [reVX](https://github.com/NREL/revx), [rex](https://github.com/NREL/rex), & [NRWAL](https://github.com/NREL/NRWAL)) is to create a conda environment and install rev through the nrel channel.

```
conda create -n rev python=3.9 -y
conda activate rev
conda install nrel-rev -c nrel
```

You can also close the repository and install directly from there. 
```
conda create -n rev python=3.9 -y
conda activate rev
git clone https://github.com/NREL/reV.git
cd reV
python setup.py install
```

Finally, to make sure that the reV CLIs are working, simply type the ```reV``` command into your terminal. If it was successfully installed you will see a printout of a help file showing the command format and a brief description of all the reV modules:

```
Usage: reV [OPTIONS] COMMAND [ARGS]...

  reV command line interface.

Options:
  --version               Show the version and exit.
  -n, --name STR          Job name. Default is "reV".
  -c, --config_file PATH  reV configuration file json for a single module.
                          [required]
  -v, --verbose           Flag to turn on debug logging. Default is not
                          verbose.
  --help                  Show this message and exit.

Commands:
  batch                     Execute multiple steps in a reV analysis...
  collect                   Collect files from a job run on multiple nodes.
  econ                      Econ analysis (lcoe, single-owner, etc...).
  generation                Generation analysis (pv, csp, windpower,...
  multi-year                Run reV multi year using the config file.
  offshore                  Offshore gen/econ aggregation with NRWAL.
  pipeline                  Execute multiple steps in a reV analysis...
  qa-qc                     Run reV QA/QC using the config file.
  rep-profiles              Run reV representative profiles using the...
  supply-curve              Run reV supply curve using the config file.
  supply-curve-aggregation  Run reV supply curve aggregation using the...
```

# Getting Started - Installating reV-tutorial

The simplest way to install reV and it's supporting packages ([PySAM](https://github.com/NREL/pysam), [reVX](https://github.com/NREL/revx), [rex](https://github.com/NREL/rex), & [NRWAL](https://github.com/NREL/NRWAL)) is to create a conda environment and install rev through the nrel channel.

```
cd ..
git clone https://github.com/WilliamsTravis/reV-tutorial.git
cd reV-tutorial
```

# Using the CLI Method
The quickest and easiest to get started with reV is to use the **JSON-CLI** workflow. This involves building a json configuration file (which is like a string of a Python dictionary) for a module you want to run and running that module with the corresponding CLI command. You can also configure several modules in an input-output pipeline and run each with a single command. The configurations will tell reV which SAM generator configurations to run and where, what variables to generate, which land-use assumptions to use, etc. It will also tell reV how to work with your system to most efficiently build these outputs (e.g. how to split the work across cpus, how to split work across nodes for distributed systems, what memory utilization limits to use, etc.). This method is convient in that you don't need to edit any Python scripts and is easy to set up and run directly from your terminal (at least for single runs). So far we only have one sample run, a simple generation pipeline. To get started, clone this repo, activate your reV environment setup above, cd into the **reV-tutorial/cli_runs/generation** directory, and open the README.md found there.
