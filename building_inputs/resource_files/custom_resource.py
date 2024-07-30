# -*- coding: utf-8 -*-
"""Building custom reV-compatible resource files.

Created on Wed Jan  5 13:21:06 2022

@author: twillia2
"""
import datetime as dt

from glob import glob

import h5py
import numpy as np
import pandas as pd

import csv

from rex.utilities.utilities import get_dtype, to_records_array


PROFILES = "./inputs/*srw" # https://samrepo.nrelcloud.org/help/weather_format_srw_wind.html


def make_meta(metas):
    """Return structure meta array out of list of meta dicts."""
    df = pd.DataFrame(metas)
    df["timezone"] = -9  # <--------------------------------------------------- We just know this
    df["elevation"] = 1_000  # <----------------------------------------------- We don't actually know this
    data = to_records_array(df)
    return data


def reformat_single(file):
    """Reformat a single time-series data file into a vector."""
    # An SRW is a format used in the SAM GUI for default resource inputs

    # It contains header information and a table
    # df = pd.read_csv(file, on_bad_lines='skip', header=None)

    with open(file, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for i, line in enumerate(reader):
            if (i == 0):
                # In this case we have unit and location information in the first 2 lines
                # HW 07292024 update: as in the SAM documentation: Row 1 must have at least 8 columns. You must provide a value for each column:
                # If you do not have a value for a column, you can use an indicator like n/a or ?? for the missing value.
                # Since we have missed original inputs, we generated a value for "year" from the output *.h5 file. 
                gid, city, state, county, year, lat, lon, _, _, steps = line
                year = 2013

            if (i == 1):
                # More descriptive info is found in the second row, first column
                description = line

            if (i == 2):
                # And header are in the thrid row with units in the 4th
                headers = line

            if (i == 3):
                units = line  # <------------------------------------------------ We will need to check units and convert if they aren't right

            if (i == 5):
                # Finally our data starts in the 6th row, extends to the 5th column
                data = pd.DataFrame([line[0:4]])

            if (i > 5):
                data.loc[len(data)] = line[0:4]



    # These headers need to be lower case and associated with a height
    headers = [  # <----------------------------------------------------------- We just know all this too
        "temperature_2m",
        "pressure_2m",
        "windspeed_100m",
        "winddirection_100m"
    ]
    data.columns = headers
    data = data.reset_index(drop=True)
    data = data.astype(float)

    # Hold onto the meta information
    meta = {"latitude": lat, "longitude": lon, "year": year, 
            "timesteps": steps, "description": description}
    return data, meta


def time(year, steps):
    """Create time index from meta data."""
    # Assume first day of the year
    time_format = "%Y-%m-%d %H:%M:%S"
    if steps == 8760:
        idx = pd.date_range(f"{int(year)}-01-01", periods=8760, freq='h')  # <- We know that it's hourly, it would be better to infer
    else:
        idx = pd.date_range(f"{int(year)}-01-01", periods=8784, freq='h')
    strings = [dt.datetime.strftime(t, time_format) for t in idx]
    return strings


def build():
    """Reformatting and packaging raw resource timeseries data into a reV."""
    # Reformat the raw data into time by site 2D arrays
    files = glob(PROFILES)
    datasets = {}
    metas = []
    for file in files:
        data, meta = reformat_single(file)
        for name, vector in data.items():
            if name not in datasets:
                datasets[name] = []
            datasets[name].append(vector.values)
        metas.append(meta)

    # Build the meta file as a structured array
    meta = make_meta(metas)

    # Merge dataset list of arrays into single 2d arrays
    merged = {}
    for name, arrays in datasets.items():
        array = np.array(arrays).T
        merged[name] = array

    # Create a vector of datetime formatted strings
    time_index = time(meta["year"][0], meta["timesteps"][0])
    time_index = [t.encode() for t in time_index]

    # Create an HDF File out of these elements
    year = int(meta["year"][0])
    ds = h5py.File(f"test_resource_{year}.h5", "w")
    for name, array in merged.items():
        ds.create_dataset(name=name, data=array)
    ds.create_dataset(name="time_index", data=time_index)
    ds.create_dataset(name="meta", data=meta)
    ds.close()


if __name__ == "__main__":
    build()
