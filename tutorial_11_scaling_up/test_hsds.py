# -*- coding: utf-8 -*-
"""Test that the HSDS server is up and running.

This test requires that a local HSDS server is setup and installed, as per the
instructions in the README.

Author: travis
Date: Wed Aug 27 09:26:00 PM MDT 2025
"""
from pathlib import Path

import h5pyd

from rex import Resource
from rex import WindX


HOME = Path(__file__).parent
HSDS_FPATH = "/nrel/nsrdb/current/nsrdb_1999.h5"
HSDS_URL = "s3://nrel-pds-nsrdb/current/nsrdb_1999.h5"
HSDS_KWARGS = {
    "hs_endpoint": "http://localhost:5101",
    "hs_bucket": "nrel-pds-hsds"
}


def main(url=False):
    """Test various ways of accessing data through HSDS."""
    # h5pyd test
    try:
        with h5pyd.File(HSDS_FPATH) as file:
            datasets = list(file)
        print(f"Success: HSDS test with h5pyd")
    except Exception as e:
        print(f"Fail: HSDS test with h5pyd")

    # rex test #1
    try:
        with Resource(HSDS_FPATH) as file:
            datasets = list(file)
        print("Success: HSDS test with rex Resource "
              f"and {HSDS_FPATH}")
    except Exception as e:
        print("Fail: HSDS test with rex Resource "
              f"and {HSDS_FPATH}")

    # rex test #2
    try:
        with Resource(HSDS_URL) as file:
            datasets = list(file)
        print("Success: HSDS test with rex Resource "
              f"and {HSDS_URL}")
    except Exception as e:
        print("Fail: HSDS test with rex Resource "
              f"and {HSDS_URL}")

   # rex test #3
    try:
        with Resource(HSDS_FPATH, hsds=True) as file:
            datasets = list(file)
        print("Success: HSDS test with rex Resource "
              f"and {HSDS_FPATH} and hsds set to True")
    except Exception as e:
        print("Fail: HSDS test with rex Resource "
              f"and {HSDS_FPATH} and hsds set to True")

    # rex test #4
    try:
        with Resource(HSDS_URL, hsds=True) as file:
            datasets = list(file)
        print("Success: HSDS test with rex Resource "
              f"and {HSDS_URL} and hsds set to True")
    except Exception as e:
        print("Fail: HSDS test with rex Resource "
              f"and {HSDS_URL} and hsds set to True")

    # rex test #5
    try:
        with Resource(HSDS_FPATH, hsds=True, hsds_kwargs=HSDS_KWARGS) as file:
            datasets = list(file)
        print("Success: HSDS test with rex Resource "
              f"and {HSDS_FPATH} and hsds set to True and explicitly setting "
             "hsds_kwargs.")
    except Exception as e:
        print("Fail: HSDS test with rex Resource "
              f"and {HSDS_FPATH} and hsds set to True and explicitly setting "
              f"hsds_kwargs: {HSDS_KWARGS}.")

    # rex test #5
    try:
        with Resource(HSDS_URL, hsds=True, hsds_kwargs=HSDS_KWARGS) as file:
            datasets = list(file)
        print("Success: HSDS test with rex Resource "
              f"and {HSDS_URL} and hsds set to True and explicitly setting "
              "hsds_kwargs.")
    except Exception as e:
        print("Fail: HSDS test with rex Resource "
              f"and {HSDS_URL} and hsds set to True and explicitly setting "
              f"hsds_kwargs: {HSDS_KWARGS}")


if __name__ == "__main__":
    main()
