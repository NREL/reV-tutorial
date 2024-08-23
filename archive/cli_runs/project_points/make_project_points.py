# Basic library imports
import pandas as pd 


# Read in the supply points -> this matches with the ID 
# This is a subset of a larger h5 file which contains all of CONUS
meta = pd.read_csv('wind_power_supply_points.csv')


# For the purposes of the tutorial we only want GID for 
# We also only want to select the wind onshore which is where offshore column=0
meta_ri = meta.loc[(meta['state']== 'Rhode Island') & 
                   (meta['offshore']== 0)].copy()

# Now you need to create a subset that contains just the gid and the config so 
# we add config to the dataframe
meta_ri['config'] = 'default'
project_points_ri = meta_ri[['gid', 'config']].copy()

# Save this to a project points file 

project_points_ri.to_csv('ri_onshore_wind_project_points.csv', index=False)