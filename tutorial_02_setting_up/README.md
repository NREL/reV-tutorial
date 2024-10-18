# Getting Started - Installing reV

The simplest way to install reV and it's supporting packages ([PySAM](https://github.com/NREL/pysam), [rex](https://github.com/NREL/rex), & [NRWAL](https://github.com/NREL/NRWAL)) is to create a virtual environment and install rev with pip.

```
python3.11 -m venv rev
source rev/bin/activate
pip install NREL-reV
```

You can also clone the repository and install directly from there. To use the ssh address (as below) and avoid having to enter your username and password, use this [guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account). 
```
python3.11 -m venv rev
source rev/bin/activate
git clone https://github.com/NREL/reV.git
cd reV
python3.11 -m pip install .
```

If you would prefer a developer's installation so that reV will pick up changes directly from the repository files, replace `python3.11 -m pip install .` above with 
```
python3.11 -m pip install -e .
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

# Testing the installation

Each new reV model version is tested on the latest Linux (Ubuntu), Windows, and MacOS operating systems. If you have a different OS or would like to double check that the all of the tests pass in your set up, use the GitHub repository method described above, and 
```
cd reV/tests/
pip install pytest
pytest .
```
This takes quite some time, so it's best if you have something else to do for a while.


# All done?
Now you may move on to Tutorial 3: Building Inputs (tutorial_3_input_builds).
