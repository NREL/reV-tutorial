Resource Files
===
The resource files used by reV contain the same information as those used by SAM but contain multiple locations (represented in a grid), have a fundamentally different structure, and are much larger in size. This format is nicely integrated into the NREL modeling ecosystem but is unique to NREL. So, it typically requires some explanation and, for new users or people with experience in more standardized atmospheric data formats like NetCDFs, it may take some time to get used to. Notably, the output generation files that reV produces will mirror the structure of this format.

The inputs required for a reV-compatible resource file will depend on the SAM module used in the generation step. The datasets you'll need to include in the file will depend on the SAM technology being modeled. You can find more information about the sets of required variables in SAM's help page here https://samrepo.nrelcloud.org/help/weather_format.html. Below, we've recreated SAM's weather variable reference table to include just the reV-comaptible modules. Note that not all elements are always required (e.g., snow losses simply won't be modeled in PV if the depth variable is missing). More notes on each variable can be found in the weather data elements page here: https://samrepo.nrelcloud.org/help/weather_data_elements.html.


<table align="center">
  <thead>
    <tr>
      <th>Variable</th>
      <th>Windpower</th>
      <th>PVSamv1</th>
      <th>PVWatts</th>
      <th>Concentrating Solar</th>
      <th>Geothermal</th>
  </tr>
  </thead>

  <tbody align="center">
    <tr><td>Latitude (decimal &deg;)</td>
      <td>*</td><td>*</td><td>*</td><td>*</td><td>*</td>
    </tr>
    <tr><td>Longitude (decimal &deg;)</td>
      <td>*</td><td>*</td><td>*</td><td>*</td><td>*</td>
    </tr>
    <tr><td>Datetime (<i>"%Y-%m-%d %H:%M:%S"</i>)</td>
      <td>*</td><td>*</td><td>*</td><td>*</td><td>*</td>
    </tr>
    <tr><td>Elevation (m)</td>
      <td>*</td><td>*</td><td>*</td><td>*</td><td></td>
    </tr>
    <tr><td>Albedo</td>
      <td></td><td>*</td><td>*</td><td></td><td></td>
    </tr>
    <tr><td>Atmospheric Pressure (mbar)</td>
      <td>*</td><td>*</td><td></td><td>*</td><td>*</td>
    </tr>
    <tr><td>Irradiance - Diffuse Horizontal (W/m<sup>2</sup>)</td>
      <td></td><td>*</td><td>*</td><td></td><td></td>
    </tr>
    <tr><td>Irradiance - Direct Normal (W/m<sup>2</sup>)</td>
      <td></td><td>*</td><td>*</td><td>*</td><td></td>
    </tr>
    <tr><td>Irradiance - Global Horizontal (W/m<sup>2</sup>)</td>
      <td></td><td>*</td><td></td><td></td><td></td>
    </tr>
    <tr><td>Irradiance - Plane of Array (W/m<sup>2</sup>)</td>
      <td></td><td>*</td><td>*</td><td></td><td></td>
    </tr>
    <tr><td>Relative Humidity (%)</td>
      <td></td><td></td><td></td><td>*</td><td>*</td>
    </tr>
    <tr><td>Snow Depth (cm)</td>
      <td></td><td>*</td><td>*</td><td></td><td></td>
    </tr>
    <tr><td>Temperature - Dew Point(&deg;C)</td>
      <td></td><td>*</td><td></td><td>*</td><td></td>
    </tr> 
    <tr><td>Temperature - Dry Bulb (&deg;C)</td>
      <td>*</td><td>*</td><td>*</td><td>*</td><td>*</td>
    </tr>
    <tr><td>Temperature - Wet Bulb (&deg;C)</td>
      <td></td><td>*</td><td></td><td>*</td><td>*</td>
    </tr>
    <tr><td>Wind Direction (&deg;)</td>
      <td>*</td><td>*</td><td></td><td></td><td></td>
    </tr>
    <tr><td>Wind Speed (m/s)</td>
      <td>*</td><td>*</td><td>*</td><td>*</td><td></td>
    </tr>
  </tbody>
</table>


The Format
===
This format is nicely integrated into the NREL modeling ecosystem but is unique to NREL, so it requires some explanation. For a high-level overview, these are the primary characteristic you'll need to know when working with these files:

- Hierarchical Data Format 5 (HDF5)
- 2D array for each data variable (GHI, Windspeed, air pressure, etc.)
- Time Index on Y-Axis
- Site Index X-Axis
- Contains a `meta` data table that holds coordinate and other site information associated with the x-axis
- Contains a 1D `time_index` vector that contains date-time strings associated with the y-axis.
- A `scale_factor` attribute on each variable that is used to translate integers back into floats where scaling is used for data storage.
- A `units` attribute that stores the units for each variable.

Examples of this format for the `windpower` and `pvwatts` modules may be found here: [https://github.com/NREL/reV-tutorial/tree/master/data/resources](../../data/resources/). 

## Visualizing reV Outputs
The graphic below shows a representation of NREL's space-time format using a reV generation output. The reV generation module's outputs mirror the resource file's format so any variable in the resource file will match this structure. This graphic shows a reV capacity factor timeseries array, a map of the average capacity factors derived from it, a glimpse at the meta data associated with the X-Axis, and a glimpse at the timeseries vector associated with the Y-Axis.

![resource_data_diagram](https://github.com/user-attachments/assets/7b14b266-3e81-4046-b2cb-b97566253b7d)

If you zoom into the red segment in the array, you can see how this format represents the daily pattern of solar irradiance across space.  In the map below, only the locations represented in this red segment are shown. In this value segment, you can also see the effect of clouds moving across this area over time, particularly from day 8 through 9 of this period.

![resource_data_diagram_zoomin](https://github.com/NREL/reV-tutorial/blob/master/data/images/resource_data_diagram_zoomin.png)

Existing Resource Files
===
`NSRDB`, the [National Solar Radiation Database](https://registry.opendata.aws/nrel-pds-nsrdb/), is a collection of half-hourly values of the three most common measurements of solar radiation – global horizontal, direct normal, and diffuse horizontal irradiance — and other meteorological data the System Advisor uses to refine energy generation estimates. These data have been collected at a sufficient number of locations and temporal and spatial scales to accurately represent regional solar radiation climates.

`WTK`, the [Wind Integration National Dataset (WIND) Toolkit](https://registry.opendata.aws/nrel-pds-wtk/), is an update and expansion of the Eastern Wind Integration Data Set and Western Wind Integration Data Set. It supports the next generation of wind integration studies. It includes instantaneous meteorological conditions from computer model output and calculated turbine power for more than 126,000 sites in the continental United States for the years 2007–2013. 

Remote ACCESS to preformatted datasets
===
  - NREL Highly Scalable Data Service (`HSDS`) [Examples](https://github.com/NREL/hsds-examples)
