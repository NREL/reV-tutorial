Resource Files
===
The inputs required for a reV-compatible resource file will depend on the SAM module used in the generation step. This format is a particular data format that is nicely integrated into the NREL modeling ecosystem but is unique to NREL. In this tutorial, we'll use the example HDF5 resource [data](../../data/resources/) to introduce the format. Advanced input building can be found under [tutorial_11_advanced_input_builds](../../tutorial_11_advanced_input_builds/README.md). 

The Format
===
- Hierarchical Data Format 5 (HDF5)
- 2D array for each data variable (GHI, Windspeed, air pressure, etc.)
- Time Index on Y-Axis
- Site Index X-Axis
- Contains a `meta` data table that holds coordinate and other site information associated with the x-axis
- Contains a 1D `time_index` vector that contains date-time strings associated with the y-axis.
- A `scale_factor` attribute that is used to translate integers back into floats where scaling is used for data storage.


Existing Resource Files
===
`NSRDB`, the [National Solar Radiation Database](https://registry.opendata.aws/nrel-pds-nsrdb/), is a collection of half-hourly values of the three most common measurements of solar radiation – global horizontal, direct normal, and diffuse horizontal irradiance — and other meteorological data the System Advisor uses to refine energy generation estimates. These data have been collected at a sufficient number of locations and temporal and spatial scales to accurately represent regional solar radiation climates.

`WTK`, the [Wind Integration National Dataset (WIND) Toolkit](https://registry.opendata.aws/nrel-pds-wtk/), is an update and expansion of the Eastern Wind Integration Data Set and Western Wind Integration Data Set. It supports the next generation of wind integration studies. It includes instantaneous meteorological conditions from computer model output and calculated turbine power for more than 126,000 sites in the continental United States for the years 2007–2013. 

Remote ACCESS to preformatted datasets
===
  - NREL Highly Scalable Data Service (`HSDS`) [Examples](https://github.com/NREL/hsds-examples)

Visualization an NSRDB resource file
===
![resource_data_diagram](https://github.com/user-attachments/assets/7b14b266-3e81-4046-b2cb-b97566253b7d)


Visualization an NSRDB resource file (Zoom in)
===
![resource_data_diagram_soomin](https://github.com/user-attachments/assets/6064d31a-cc45-4569-833c-95a94944ea40)
