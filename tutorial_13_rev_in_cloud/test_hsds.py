"""Test resource data access through HSDS."""
from urllib3.exceptions import HTTPError

import h5pyd

from rex.resource import Resource


SAMPLE_FPATH = "/nrel/nsrdb/conus/nsrdb_conus_2019.h5"


def test_h5pyd():
    """Test resource data access with h5pyd."""
    with h5pyd.File(SAMPLE_FPATH) as file:
        try:
            _ = file["ghi"][:, :100]
            print("HSDS h5pyd resource data access test: passed")
        except HTTPError:
            print("HSDS h5pyd resource data access test: failed")



def test_rex():
    """Test resource data access with rex."""
    with Resource(SAMPLE_FPATH) as file:
        try:
            _ = file["ghi", :, :100]
            print("HSDS rex resource data access test: passed")
        except Exception as e:
            print("HSDS rex resource data access test: failed: {e}")


if __name__ == "__main__":
    test_h5pyd()
    test_rex()
