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

The format is composed of a set of non-grouped HDF5 datasets and attributes. Atmospheric datasets are stored as 2D arrays whose index positions correspond to separate datasets containing a 1D datetime vector and a 2D structured meta data array (which stores the coordinates and site-specifc information). Each data variable (aside from the meta and time datasets) will have attributes for at least a scale factor and a units string. Additional attributes on either the individual datasets or the file itself may also be stored to help users understand the file's contents. The main characteristics needed to understand this format are outlined below:

- Hierarchical Data Format 5 (HDF5)
- 2D array for each data variable (GHI, windspeed, air pressure, etc.)
- Time index on Y-Axis
- Site index X-Axis
- Contains a `meta` data table that holds coordinate and other site information associated with the x-axis
- Contains a 1D `time_index` vector that contains date-time strings associated with the y-axis
- A `scale_factor` attribute on each variable that is used to translate integers back into floats where scaling is used for data storage
- A `units` attribute that stores the units for each variable

Examples of this format for the `windpower` and `pvwatts` modules may be found here: [https://github.com/NREL/reV-tutorial/tree/master/data/resources](../../data/resources/). 

## Visualizing the format through reV Outputs
The graphic below shows a representation of NREL's space-time format using a `reV` output. The `reV generation` and `rep-profiles` outputs mirror the resource file's format so any variable in the resource file will match this structure. This graphic shows a reV capacity factor timeseries array, a map of the average capacity factors derived from it, a glimpse at the meta data associated with the X-Axis, and a glimpse at the timeseries vector associated with the Y-Axis.

![resource_data_diagram](https://github.com/user-attachments/assets/7b14b266-3e81-4046-b2cb-b97566253b7d)

<br>

If you zoom into the red segment in the array, you can see how this format represents the daily pattern of solar irradiance across space.  In the map below, only the locations represented in this red segment are shown. In this value segment, you can also see the effect of clouds moving across this area over time, particularly from day 8 through 9 of this period.

<br>


![resource_data_diagram_zoomin](https://github.com/NREL/reV-tutorial/blob/master/data/images/resource_data_diagram_zoomin.png)

Existing Resource Files
===

The [National Solar Radiation Database](https://registry.opendata.aws/nrel-pds-nsrdb/) (NSRDB), is a collection of half-hourly values at 4km of the three most common important measurements of solar radiation – global horizontal, direct normal, and diffuse horizontal irradiance — and other meteorological data the System Advisor uses to refine energy generation estimates. It is updated annually and represents every year since 1999.

The [Wind Integration National Dataset Toolkit](https://registry.opendata.aws/nrel-pds-wtk/) (WTK), is a collection of hourly values with a 2km spatial resolution at 20m elevation increments representing wind speed, wind direction, and other meteorological data needed to accurately model wind power. The WTK contains yearly data from 2007-2013.

Remote Access using `rex` and `HSDS`
===

NREL's resource data is remotely accessible using the HDF Group's Highly Scalable Data Service (`HSDS`). NREL's Resource Extraction Tool (rex), which is integrated into reV, allows users to seemlessly integrate remote resource access into the reV modeling pipeline, though some setup is required. For more guidance on how to setup your computer or server to access NREL data remotely, visit the rex [HSDS guide](https://nrel.github.io/rex/misc/examples.hsds.html). 

