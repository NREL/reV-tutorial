"""How to build a project points file."""
import os

import h5py
import pandas as pd 

from rex import Resource

from rev_tutorial import DATA


# Path to the HDF5 resource file
RES_FILE = DATA.joinpath("ri_100_nsrdb_2012.h5")


def main():
    """Read, format, and write a project points file."""
    # Use rex's Resource class to pull out a formatted resource meta dataframe
    with Resource(RES_FILE) as res:
        meta = res.meta

    # The "gid" column is the original index and tell reV where to run
    meta.loc[:, "gid"] = meta.index

    # Now you can subset, as long as the gid refers to the original index
    meta = meta[meta["population"] < 10_000]

    # The config column tell reV which SAM config to run
    # Here we are assuming a single 'default' config will be run every where
    meta.loc[:, "config"] = "default"

    # All reV needs is config and gid, but you can include other fields
    project_points = meta[['latitude', 'longitude', 'gid', 'config']]

    # Save this to a project points file 
    fname = "project_points.csv"
    dst = HOME.joinpath(f"tutorial_3_input_builds/make_project_points/{fname}")
    project_points.to_csv(dst, index=False)


if __name__ == "__main__":
    main()
