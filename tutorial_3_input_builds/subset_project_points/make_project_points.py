# Basic library imports
import h5py
import os
import pandas as pd 


# Path to the hdf5 file
h5file = "data/*.h5"

def decode(h5):
    """Decode the columns of a meta data object from a h5 file."""
    import ast

    def decode_single(x):
        """Try to decode a single value, pass if fail."""
        try:
            x = x.decode()
        except UnicodeDecodeError:
            x = "indecipherable"
        return x

    for c in h5.columns:
        x = h5[c].iloc[0]
        if isinstance(x, bytes):
            try:
                h5[c] = h5[c].apply(decode_single)
            except Exception:
                h5[c] = None
                print("Column " + c + " could not be decoded.")
        elif isinstance(x, str):
            try:
                if isinstance(ast.literal_eval(x), bytes):
                    try:
                        h5[c] = h5[c].apply(
                            lambda x: ast.literal_eval(x).decode()
                        )
                    except Exception:
                        h5[c] = None
                        print("Column " + c + " could not be decoded.")
            except:
                pass
    return h5

def get_hdf5_meta(path):
    """Read and format the wtk dataset."""
    with h5py.File(path, "r") as ds:
        meta = pd.DataFrame(ds["meta"][:])
    meta = decode(meta)
    meta = meta[
    (meta["country"] == "United States")    
    ]  
    # meta.loc[:, "wtk_gid"] = meta.index
    return meta


# # Read in the supply points -> this matches with the ID 
# # This is a subset of a larger h5 file which contains all of CONUS
# meta = pd.read_csv('wind_power_supply_points.csv')

# Get the formatted metadata from a hdf5 file
meta = get_hdf5_meta(h5file)

# For the purposes of the tutorial we only want GID for 
# We also only want to select the wind onshore which is where offshore column=0
meta_ri = meta.loc[(meta['state']== 'Rhode Island') & 
                   (meta['offshore']== 0)].copy()

# Now you need to create a subset that contains just the gid and the config so 
# we add config to the dataframe
meta_ri['config'] = 'default'
project_points_ri = meta_ri[['gid', 'config']].copy()

# Save this to a project points file 
# project_points_ri.to_csv('ri_onshore_wind_project_points.csv', index=False)