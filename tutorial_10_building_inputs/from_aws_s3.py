# -*- coding: utf-8 -*-
"""Get and subset resource data from NREL's AWS s3 bucket.

This scripts requires a running local HSDS server. This takes a few extra steps
but will be useful for users with large study areas because there are usage
limits when accessing resource data directly from NREL servers. Setup a local
HSDS server using this guide:
    https://nrel.github.io/rex/misc/examples.hsds.html#setting-up-a-local-\
    hsds-server

Author: travis
Date: Wed Aug 13 05:59:24 PM MDT 2025
"""
import os
import sys
import time

from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import h5py
import h5pyd
import numpy as np
import pandas as pd

from rex.utilities.utilities import to_records_array
from rex.resource import BaseResource
from tqdm import tqdm


HOME = Path(__file__).parent
ARGS = sys.argv
PARAMETERS = {
    "dst": None,
    "res_fpath": None,
    "state": None
}
SAMPLE_RES_FPATH = "/nrel/wtk/conus/wtk_conus_2011.h5"
SAMPLE_STATE = "Colorado"
SAMPLE_DST = HOME.joinpath("wtk_conus_colorado_2011.h5")


def get(res_fpath, dst, state=None, overwrite=False, ncpu=None,
        sites_per_cpu=None):
    """Get the resource data, subset, and write to file.

    Parameters
    ----------
    res_fpath : str | pathlib.PosixPath
        Path to source resource file.
    dst : str | pathlib.PosixPath
        Path to a target file.
    state : str
        Name of US state to subset results with, defaults to None, or all
        states.
    overwrite : bool
        Overwrite file and rewrite datasets, defaults to False.
    ncpu : int
        How many cpu workers to use. Defaults to None, which triggers all
        availabile cores.
    sites_per_cpu : int
        How many sites to read in per individual worker. Defaults to None,
        which chooses the minimum between 5,000 sites (an apparent maximum for
        this data) or an even distribution of all sites between each worker.
    """
    # Infer appropriate mode
    mode = "w"
    if overwrite and Path(dst).exists():
        os.remove(res_fpath)
    if Path(dst).exists():
        mode = "a"

    # Open target file
    with h5py.File(dst, mode) as target:
        # Read in meta
        with h5pyd.File(res_fpath) as src:
            print(f"Reading in meta data table from {res_fpath}...")

            # Subset meta if given a state
            meta = pd.DataFrame(src["meta"][:])
            meta = BaseResource.df_str_decode(meta)
            idx = list(meta.index)
            if state is not None:
                print(f"Subsetting to {state.lower().title()}...")
                meta = meta[meta["state"] == state.title()]
                idx = list(meta.index)

            # Write top-level attributes to new file
            for key, attr in src.attrs.items():
                target.attrs[key] = attr

            # Coordinates, meta, and time index require different approach
            if "meta" not in target:
                coords = src["coordinates"][idx, :]
                time = src["time_index"]
                smeta = to_records_array(meta)
                target.create_dataset("coordinates", data=coords)
                target.create_dataset("time_index", data=time)
                target.create_dataset("meta", data=smeta)

            # Write subsets to new file
            for key, data in src.items():
                if key not in target:
                    print(f"Writing {key} to {dst}...")
                    try:
                        data = get_dataset(res_fpath, key, idx, ncpu,
                                           sites_per_cpu)
                    except Exception as e:
                        try:
                            print(f"Error on {res_fpath}/{key} ({e}), "
                                  "trying again...")
                            data = get_dataset(res_fpath, key, idx, ncpu,
                                               sites_per_cpu)
                        except Exception as e:
                            msg = f"Can't read {key} from {res_fpath}: {e}."
                            raise Exception(msg)

                    target.create_dataset(key, data=data)

                # Write dataset attributes
                for akey, attr in src[key].attrs.items():
                    target[key].attrs[akey] = attr


def _get_chunk(res_fpath, key, cidx):
    """Retrieve data from an open HDF5 file.

    Parameters
    ----------
    res_fpath : str | pathlib.PosixPath
        Path to a resource file.
    key : str
        The name of the target dataset
    cidx : np.array
        A chunk of index position

    Returns
    -------
    np.ndarray
        A 2D array of target data. Time on the first axis, location on second.
    """
    with h5pyd.File(res_fpath) as src:
        data = src[key][:, cidx]
    return data


def get_dataset(res_fpath, key, idx, ncpu=None, sites_per_cpu=None):
    """Retrieve data from an open HDF5 file.

    Parameters
    ----------
    res_fpath : str | pathlib.PosixPath
        Path to an NREL-formatted resource file.
    key : str
        Target dataset name.
    idx : np.array
        Target index positions (optional).
    ncpu : int
        How many cpu workers to use. Defaults to None, which triggers all
        availabile cores.
    sites_per_cpu : int
        How many sites to read in per individual worker. Defaults to None,
        which chooses the minimum between 5,000 sites (an apparent maximum for
        this data) or an even distribution of all sites between each worker.

    Returns
    -------
    np.ndarray
        A 2D array of target data. Time on the first axis, location on second.
    """
    # We appear to be limited to around 5,000 sites at a time
    if not ncpu:
        ncpu = os.cpu_count()
    if not sites_per_cpu:
        sites_per_cpu = min(len(idx) // ncpu, 5_000)
    n = len(idx) // sites_per_cpu
    cidx = np.array_split(idx, n)

    # Read data in chunks
    data = []
    with ProcessPoolExecutor(ncpu) as pool:
        jobs = [pool.submit(_get_chunk, res_fpath, key, cid) for cid in cidx]
        for job in tqdm(jobs):
            data.append(job.result())

    # Combine data and return
    data = np.concat(data, axis=1)

    return data


def get_hsds_args():
    """Read in HSDS configuration arguments."""
    args = {}
    with open(Path("~/.hscfg").expanduser(), "r") as r:
        for line in r.readlines():
            key, value = line.split(" = ")
            value = value.replace("\n", "")
            key = key.replace("hs_", "")
            args[key] = value
    return args


def get_params():
    """Collect user arguments."""
    params = PARAMETERS.copy()
    if len(ARGS) > len(PARAMETERS) + 1:
        raise KeyError("Too many arguments.")
    for i, arg in enumerate(ARGS[1:]):
        key = list(params)[i]
        params[key] = arg
    return params


def main(overwrite=False, ncpu=None, sites_per_cpu=None):
    """Read, subset, and write target NREL resource data.

    Parameters
    ----------
    overwrite : bool
        Overwrite file and rewrite datasets, defaults to False.
    ncpu : int
        How many cpu workers to use. Defaults to None, which triggers all
        availabile cores.
    sites_per_cpu : int
        How many sites to read in per individual worker. Defaults to None,
        which chooses the minimum between 5,000 sites (an apparent maximum for
        this data) or an even distribution of all sites between each worker.
    """
    # Start timer
    start = time.time()

    # Get user parameters
    params = get_params()
    params["overwrite"] = overwrite  # move to args
    params["ncpu"] = ncpu
    params["sites_per_cpu"] = sites_per_cpu

    # Use user parameters or examples
    if params["dst"] is None:
        params["dst"] = str(SAMPLE_DST)
    if params["res_fpath"] is None:
        params["res_fpath"] = str(SAMPLE_RES_FPATH)
    if params["state"] is None:
        params["state"] = SAMPLE_STATE

    # Print build parameters
    print(f"Retrieving resource file with following parameters: {params}")

    # Get the dataset
    if params["res_fpath"] is not None:
        get(**params)
    else:
        raise KeyError("More parameters needed")

    # End timer
    end = time.time()
    duration = (end - start) / 60
    print(f"File written to {dst}, {duration:.2f} minutes.")


if __name__ == "__main__":
    res_fpath = SAMPLE_RES_FPATH
    dst = SAMPLE_DST
    state = SAMPLE_STATE
    overwrite = False
    ncpu = 12
    sites_per_cpu = None
    main(overwrite=overwrite, sites_per_cpu=sites_per_cpu, ncpu=ncpu)
