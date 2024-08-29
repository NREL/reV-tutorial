## Bulding Custom Resource Files

The inputs required for a reV-compatible resource file will depend on the SAM module used in the generation step. These can be found in the SAM documentation here: [SAM Help](https://samrepo.nrelcloud.org/help/index.html)


## Access the NSRDB Datasets
https://registry.opendata.aws/nrel-pds-nsrdb/


## Access the metadata for the wind toolkit
https://data.nrel.gov/submissions/54
https://www.nrel.gov/grid/wind-toolkit.html

## Descriptions to SRW format for wind resource data. Note: SAM 2022 version supports CSV format for wind.
https://samrepo.nrelcloud.org/help/weather_format_srw_wind.html



### Things to do
Finish the script, and perhaps use different input datasets. The SRWs are too awkward, and too much of it is pulling out the right meta information. 

Describe minimum inputs for each tech, or else how to figure out where to find this informations.

Describe the attributes, meta file, time index, shape of the arrays.

Show a nice image of a resource array with labels on the axis, point out a site on the x-axis and time period on the y-axis.
Fastforward to a generation file and point out the same items in it.
Go back to the meta file and point out the row with that site.


