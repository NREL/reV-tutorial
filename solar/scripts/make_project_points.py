import h5py as h5
import pandas as pd
from rex import Resource
#To make the project points we go into the resource file and pull out the meta table
# We use rex: https://github.com/NREL/rex

# Points to the file path of the resource file we want to pull from
# This is generally a h5 file for this example we are using NSRDB Rhode Island
filepath = '../rev/generation/data/ri_100_nsrdb_2012.h5'

# Using Resource from rex we pull the meta data
rs = Resource(filepath)
meta = rs.meta

# add gid -> sometimes the file doesn't have a gid which is needed
meta = meta.reset_index()
# We then select the points that are only in Rhode Island
meta_ri = meta.loc[(meta['state']== 'Rhode Island')].copy()

# Now you need to create a subset that contains just the gid and the config so we add config to the dataframe
meta_ri['config'] = 'default'
project_points_ri = meta_ri[['gid', 'config']].copy()

# Save this to a project points file 
project_points_ri.to_csv('../rev/generation/data/rhode_island_onshore_solar_project_points.csv', index=False)

