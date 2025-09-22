# Getting Started - Installing reV

Installation instructions are outlined in the reV repository ([reV](https://github.com/NREL/reV)), but we'll review them here to add more detail and a few more tips. The simplest way to install reV and it's two main dependencies ([PySAM](https://github.com/NREL/pysam) and [rex](https://github.com/NREL/rex)) is to create a virtual environment and install reV with pip. This requires a Python 3 installation, which uses a different process for each operating system. In case you need help with that, OS-dependent installation instructions can be found [here](https://wiki.python.org/moin/BeginnersGuide/Download).

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

You can also clone the repository and install directly from there. Here is an example set of unix-commands.
```bash
python3 -m venv ~/envs/rev
source ~/envs/rev/bin/activate
mkdir ~/gitrepos && cd ~/gitrepos
git clone https://github.com/NREL/reV.git
cd reV
python3 -m pip install .
```

If you prefer an editable mode, which allows modifications to the source code without needing to reinstall the package, you can replace `python3 -m pip install .` above with: 

```bash
python3 -m pip install -e .
```

Finally, to make sure that the reV CLIs are working, simply type the ```reV``` command into your terminal. If it was successfully installed you will see a printout of a help file showing the command format and a brief description of all the reV modules:

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

# Activate the reV environment as an alias

For convenience, assuming you're using a bash terminal, you can add an alias to your bash run command script (`~/.bashrc`) to call the reV activation command. Here, you can either use any text editor (nano, vim, vscode, etc.) or you can append the alias setting command directly to the end of the file with the following commands:

```bash
echo 'alias "arev=source ~/envs/rev/bin/activate"' >> ~/.bashrc  # Use whatever you want (`arev` stands for "activate rev" here)
source ~/.bashrc
```

# Testing the installation

Each new reV model version is tested on the latest Linux (Ubuntu), Windows, and MacOS operating systems, though Windows may cause some issues. Each of these test use Rhode Island as a study area. So, if you have a different OS or would like to double check that the all of the tests pass in your setup, use the GitHub repository method and the developer's installation method described above, install `pytest`, move into the `tests` directory and run the `pytest` command on that directory.
```bash
cd reV/tests/
pip install pytest
pytest .
```
This takes quite some time, but it is possible to run these tests in parallel. One way to do this is to use the `pytext-xdist` package, as shown below. Regardless of you run in parallel or serially, some of these tests are large (especially `test_bespoke.py`, so it's best if you have something else to do for a while. Below updates the above routine to run the tests with all available CPU cores.
```bash
cd reV/tests/
pip install pytest pytest-xdist
pytest -n auto .
```

# All done?
Move on to [`Tutorial 3: Building Inputs (tutorial_3_input_builds)`](https://github.com/NREL/reV-tutorial/tree/master/tutorial_03_input_builds).
