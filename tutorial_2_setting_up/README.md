# Getting Started - Installing reV

The simplest way to install reV and it's supporting packages ([PySAM](https://github.com/NREL/pysam), [reVX](https://github.com/NREL/revx), [rex](https://github.com/NREL/rex), & [NRWAL](https://github.com/NREL/NRWAL)) is to create a conda environment and install rev through the nrel channel.

```
conda create -n rev python=3.11 -y
conda activate rev
pip install NREL-reV
```

You can also clone the repository and install directly from there. 
```
conda create -n rev python=3.11 -y
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

# Getting Started - Installing reV-tutorial

To install `reV-tutorial`, follow below steps to clone the repository. 
From your home dir: 

```
git clone https://github.com/WilliamsTravis/reV-tutorial.git
cd reV-tutorial
