# Scaling reV runs

So far we've looked at running reV with a small set of sample points. This
tutorial will guide users who need larger sample areas or longer simulation
periods. In this guide we look at:

1) Accessing wind and solar resource data from NREL servers using HSDS.
2) Writing subsets of resource data to a local file system to take advantage of faster read/write times.
3) Using the multi-year module to run multiple resource years and aggregate outputs.
4) Monitoring and configuring compute resource usage.

## Accessing Resource Data using HSDS

One option available to users who want to run larger subsets of data is to setup a local HSDS server that will stream resource directly into reV. A more detailed guide on setting this up can be found in the reV documenation (https://nrel.github.io/rex/misc/examples.hsds.html#setting-up-a-local-hsds-server), but this guide will step through the process as well.


### Install dependencies

You may have installed the Resource Extraction Tool (rex) in previous tutorials, but this installation will require an additional Python dependency (h5pyd). You may install that package if already have rex or you can install an HSDS compatible rex into your reV environment with the following command:

```bash
user@host:~$ python -m pip install "nrel-rex[hsds]>=0.2.88"
```

Once you've done that, you'll need to configure HSDS to point to NREL's AWS S3 bucket where the resource data is housed. This involves setting the system parameters below in your terminal shell. 

```
export AWS_S3_GATEWAY=http://s3.us-west-2.amazonaws.com
export AWS_S3_NO_SIGN_REQUEST=1
```

To avoid having to rerun these commands everytime, you can add these lines to your `~/.bashrc` file.

Then configure your HSDS server to point to the NREL AWS s3 bucket. You can either write the following lines to a file named `~/.hscfg` or run `hsconfigure` and enter the appropriate lines when prompted:

```
hs_endpoint = http://localhost:5101
hs_bucket = nrel-pds-hsds
```

Then, run `hsds` and after a few seconds you should see an output that indicates that the HSDS service is ready. More details can be found in the guide linked above, but a quick (and useful) way to check that it's working properly is to open a new shell and use the `hsls` command to navigate the HSDS file system. This works similarly to the Unix `ls` command, but you have to use a trailing forward slash when listing directory contents (e.g., `hsls /nrel/` for all resource directories). To list all datasets in a single HDF5 file, just call `hsls` directly on the file:

```bash
user@host:~$ hsls /nrel/wtk/conus/wtk_conus_2013.h5

coordinates Dataset {2488136, 2}
inversemoninobukhovlength_2m Dataset {8760, 2488136}
meta Table {2488136}
precipitationrate_0m Dataset {8760, 2488136}
pressure_0m Dataset {8760, 2488136}
pressure_100m Dataset {8760, 2488136}
pressure_200m Dataset {8760, 2488136}
relativehumidity_2m Dataset {8760, 2488136}
temperature_100m Dataset {8760, 2488136}
...
```

You can check things like dataset attributes, see all your options with `hsls --help`.

```bash
user@host:~$ hsls --showattrs /nrel/wtk/conus/wtk_conus_2013.h5/windspeed_100m

windspeed_100m/ Dataset {8760, 2488136}
   attr: fill_value               65535
   attr: scale_factor             100.0
   attr: units                    m s-1
```


## Accessing Resource Data using NREL's AWS bucket

To use remote resource data for a reV run, you'll need to access this data at two points in the process: 1) to build your project point file and 2) to enable reV to pipe this data through to PySAM.

The process we typically use for building a project point file is virtually the same as it is with a local file, except that you'll need to use the `h5pyd` package instead of the `h5py` package. Below is an example that walks you through building a project point file for a PV run in Colorado. It assumes you have successfully set up an HSDS server and that it is running in the background. There's also a python script that recreates this in this folder.

```python
import h5pyd
import pandas as pd

from rex.resource import BaseResource

# Find your paths and select your target state
FPATH = "/nrel/nsrdb/current/nsrdb_1998.h5"
STATE = "Colorado"
DST = "./sample_hsds_run/project_points_nsrdb_colorado.csv"

# Read in the meta table from one of your target dataset files
with h5pyd.File(FPATH) as file:
    meta = pd.DataFrame(file["meta"][:])
    meta = BaseResource.df_str_decode(meta)  # Decodes byte strings

# Find the indices associated with your state
points = meta[meta["state"] == STATE].copy()
points.loc[:, "gid"] = points.index
points.loc[:, "config"] = "default"

# Write to file, done
points.to_csv(DST, index=False)
```

Then, you'll have to enter the appropriate paths in your generation
configuration file. There is a set of example configs you can experiement with
in `./


## The Multi-year Module

## Monitoring and Configuring Compute Resource Usage

