# -*- coding: utf-8 -*-
"""Example for building a project points file with HSDS accessed NREL resource
data.

Author: travis
Date: Tue Aug 26 03:53:36 PM MDT 2025
"""
from pathlib import Path

import pandas as pd
import h5pyd

from rex.resource import BaseResource


HOME = Path(__file__).parent
FPATH = "/nrel/nsrdb/current/nsrdb_1998.h5"
STATE = "Colorado"
DST = HOME.joinpath("sample_hsds_run/project_points_nsrdb_colorado.csv")


def main():
    """Build a Colorado NSRDB project points file with a HSDS-accessed file."""
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


if __name__ == "__main__":
    main()
