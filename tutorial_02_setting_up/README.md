# Getting Started - Installing reV

Installation instructions are outlined in the reV repository ([reV](https://github.com/NREL/reV)) and [rex](https://github.com/NREL/rex)), but we'll review them here to make sure you get it. The simplest way to install reV and it's two main dependencies ([PySAM](https://github.com/NREL/pysam) and [rex](https://github.com/NREL/rex)) is to create a virtual environment and install rev with pip. This requires a Python 3 installation, which uses a different process for each operating system. In case you need help with that, OS-dependent installation instructions can be found [here](https://wiki.python.org/moin/BeginnersGuide/Download).

Unix:
```
mkdir ~/envs
python3 -m venv ~/envs/rev
source ~/envs/rev/bin/activate
pip install NREL-reV
```

Windows:
```
mkdir ~/envs
python3 -m venv ~/envs/rev
.\env\Scripts\activate.bat
pip install NREL-reV
```

You can also clone the repository and install directly from there. Here is an example set of unix-commands.
```
python3 -m venv ~/envs/rev
source ~/envs/rev/bin/activate
mkdir ~/github && cd ~/github
git clone https://github.com/NREL/reV.git
cd reV
python3 -m pip install .
```

If you prefer an editable mode, which allows modifications to the source code without needing to reinstall the package, you can replace `python3 -m pip install .` above with: 

```
python3 -m pip install -e .
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

Each new reV model version is tested on the latest Linux (Ubuntu), Windows, and MacOS operating systems, though Windows may cause some issues. If you have a different OS or would like to double check that the all of the tests pass in your set up, use the GitHub repository method and the developer's installation method described above, and 
```
cd reV/tests/
pip install pytest
pytest .
```
This takes quite some time, (particularly `test_bespoke.py`) so it's best if you have something else to do for a while.


# All done?
Now you may move on to Tutorial 3: Building Inputs (tutorial_3_input_builds).
