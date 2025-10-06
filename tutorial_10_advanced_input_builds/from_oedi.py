# -*- coding: utf-8 -*-
"""Build a resource file from the Open Energy Data Initiative.

Resource data it stored on AWS, but can easily retrieved through OEDI's AWS
S3 Explorer (e.g., https://data.openei.org/s3_viewer?bucket=nrel-pds-wtk).
However, these files represent large domains and are quite large (many TBs
each). So, this script shows you a way to access subsets of this data and write
to local files for use in reV.

Author: travis
Date: Wed Aug 13 02:30:20 PM MDT 2025
"""
from pathlib import Path

import xarray as xr


HOME = Path(__file__).parent
SRC = "s3://nrel-pds-wtk/conus/v1.0.0/wtk_conus_2013.h5"


class NRELResourceFormat:
    """Methods for writing energy resource data into NREL's format."""

    def __init__(self, src):
        """Initialize an NRELResourceFormat object.

        Parameters
        ----------
        src : str | pathlib.PosixPath
            Path to original resource file. Can be a path to a local or remote
            file system.
        """
        self.src = src

    def __repr__(self):
        """Return an NRELResourceFormat object representation string."""
        address = hex(id(self))
        msgs = [f"\n   {k}={v}" for k, v in self.__dict__.items()]
        msg = ", ".join(msgs)
        return f"<NRELResourceFormat object at {address}>: {msg}"

    def to_nrel(self, dst):
        """Write the data to an NREL-formatted HDF5 file.

        Parameters
        ----------
        dst : str | pathlib.PosixPath
            Local path to output file.
        """
        # Open file
        ds = xr.open_dataset(self.src, engine="rex", chunks="auto")

        # Subset
        ds


def main():
    """A docstring."""


if __name__ == "__main__":
    self = NRELResourceFormat(src=SRC)
