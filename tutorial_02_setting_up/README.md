# Getting Started - Installing reV

Installation instructions are outlined in the reV repository ([reV](https://github.com/NREL/reV)), but we'll review them here to add more detail and a few more tips. The simplest way to install reV and its two main dependencies ([PySAM](https://github.com/NREL/pysam) and [rex](https://github.com/NREL/rex)) is to create a virtual environment and install reV with pip. This requires a Python 3 installation, which uses a different process for each operating system. In case you need help with that, OS-dependent installation instructions can be found [here](https://wiki.python.org/moin/BeginnersGuide/Download).

## Check Python Version
Make sure that the Python version you are using is compatible with reV. To do this, call the command below and check it against the supported Python versions found on the reV GitHub repository page.
```bash
python3 --version
```

## Basic Installation
Unix:
```bash
mkdir ~/envs
python3 -m venv ~/envs/rev
source ~/envs/rev/bin/activate
pip install NREL-reV
```

Windows:
```bash
mkdir ~/envs
python3 -m venv ~/envs/rev
.\envs\rev\Scripts\activate.bat
pip install NREL-reV
```

If you plan on retrieving resource data remotely from NREL servers, you need to install reV with HSDS support. Just add the `[hsds]` option to the pip installation command as follows:
```bash
pip install NREL-reV[hsds]
```


## First Check - Run the `reV` CLI command
Next, let's do a quick check to see if reV was successfully installed on your system: simply type the ```reV``` command into your terminal. If it was successfully installed you will see a printout of a help file showing the command format and a brief description of all the reV modules:

```bash
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


## Activate the reV environment as an alias

For convenience, assuming you're using a bash terminal, you can add an alias to your bash run command script (`~/.bashrc` for Linux or `~/.bash_profile` for MacOS) to call the reV activation command. You can use any text editor (nano, vim, vscode, etc.) and add `alias arev="source ~/envs/rev/bin/activate"` to the bottom somewhere. Here, `arev` stands for "activate rev", but you can call it whatever you want. You can also append the alias setting command to the end of the file directly with the following command:

```bash
echo -e '\n# Activate the reV environment\nalias arev="source ~/envs/rev/bin/activate"' >> ~/.bashrc
```
After that, to use the command in the same session, you'll have to run your bash run command script again with the following command. This will run automatically the next time you open a new terminal session.

```bash
source ~/.bashrc
```

## Install from source
You can also clone the repository and install directly from there. Here is an example set of unix-commands.
```bash
python3 -m venv ~/envs/rev
source ~/envs/rev/bin/activate
mkdir ~/gitrepos && cd ~/gitrepos
git clone https://github.com/NREL/reV.git
cd reV
python3 -m pip install .
```

## Install from source in editable mode
If you prefer an editable mode, which allows modifications to the source code without needing to reinstall the package, you can replace `python3 -m pip install .` above with: 

```bash
python3 -m pip install -e .
```

## Second Check - Testing the installation
Finally, you may want to thoroughly test your installation if you plan on doing large scale production runs. Each new reV model version is tested on the latest Linux (Ubuntu), Windows, and MacOS operating systems, though Windows may cause some issues. Each of these test use Rhode Island as a study area. So, if you have a different OS or would like to double check that the all of the tests pass in your setup, use the GitHub repository method and the developer's installation method described above, install `pytest`, move into the `tests` directory and run the `pytest` command on that directory.
```bash
cd reV/tests/
pip install pytest
pytest .
```
This takes quite some time, but it is possible to run these tests in parallel. One way to do this is to use the `pytest-xdist` package, as shown below. Regardless of you run in parallel or serially, some of these tests are large (especially `test_bespoke.py`, so it's best if you have something else to do for a while). Below updates the above routine to run the tests with all available CPU cores.
```bash
cd reV/tests/
pip install pytest pytest-xdist
pytest -n auto .
```

## All done?
Move on to [`Tutorial 3: Building Inputs (tutorial_3_input_builds)`](https://github.com/NREL/reV-tutorial/tree/master/tutorial_03_input_builds).
