# Getting Started - Installating reV

The simplest way to install reV and it's supporting packages ([PySAM](https://github.com/NREL/pysam), [reVX](https://github.com/NREL/revx), [rex](https://github.com/NREL/rex), & [NRWAL](https://github.com/NREL/NRWAL)) is to create a conda environment and install rev through the nrel channel.

```
conda create -n rev python=3.11 -y
conda activate rev
conda install nrel-rev -c nrel
```

You can also clone the repository and install directly from there. 
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
  generation                Generation analysis (pv, csp, windpower,..).
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


# An excellent resource for learning about reV:
https://nrel.github.io/reV/_cli/cli.html
