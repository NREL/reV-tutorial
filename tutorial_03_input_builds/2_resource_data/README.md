Bulding Custom Resource Files
===
The inputs required for a reV-compatible resource file will depend on the SAM module used in the generation step. This format is a particular data format that is nicely integrated into the NREL modeling ecosystem but is unique to NREL. 

The Format
===
- Hierarchical Data Format 5 (HDF5)
- 2D array for each data variable (GHI, Windspeed, air pressure, etc.)
- Time Index on Y-Axis
- Site Index X-Axis
- Contains a `meta` data table that holds coordinate and other site information associated with the x-axis
- Contains a 1D `time_index` vector that contains date-time strings associated with the y-axis.


Existing Resource Files
===
`NSRDB`, the National Solar Radiation Database, is a serially complete collection of hourly and half-hourly values of the three most common measurements of solar radiation – global horizontal, direct normal, and diffuse horizontal irradiance — and meteorological data. These data have been collected at a sufficient number of locations and temporal and spatial scales to accurately represent regional solar radiation climates.
  - https://registry.opendata.aws/nrel-pds-nsrdb/

`WTK`, the Wind Integration National Dataset (WIND) Toolkit, is an update and expansion of the Eastern Wind Integration Data Set and Western Wind Integration Data Set. It supports the next generation of wind integration studies. It includes instantaneous meteorological conditions from computer model output and calculated turbine power for more than 126,000 sites in the continental United States for the years 2007–2013. 
  - https://registry.opendata.aws/nrel-pds-wtk/


Remote ACCESS to preformatted datasets
===
  - NREL Highly Scalable Data Service (`HSDS`) Examples: https://github.com/NREL/hsds-examples


Things to do
===

Show a nice image of a resource array with labels on the axis, point out a site on the x-axis and time period on the y-axis.
Fastforward to a generation file and point out the same items in it.
Go back to the meta file and point out the row with that site.

Info before 2024
===
Some reminders for building custom resource files:
  1) You can use h5py and pandas to build it.
  2) You'll need a specific set of needed input datasets for the SAM power module you're using.
  3) For pvwattsv7, if you have any 2 out of the "ghi", "dni", or "dhi" inputs reV will calculate the third for you.
  4) The meta table must be included as the "meta" dataset. Each row corresponds to the x-position of the corresponding resource time series array. It must be converted to a structured array before you can store it and HDF5 file. If you have a pandas data frame you can use the following function to convert it:      
  
    def to_sarray(df):
        """Create a structured array for storing in HDF5 files.
    
        Parameters
        ----------
        df : pandas.core.frame.DataFrame
          Meta file.
        """
        # For a single column
        def make_col_type(col, types):

            coltype = types[col]
            column = df.loc[:, col]

            try:
                if 'numpy.object_' in str(coltype.type):
                    maxlens = column.dropna().str.len()
                    if maxlens.any():
                        maxlen = maxlens.max().astype(int)
                        coltype = ('S%s' % maxlen)
                    else:
                        coltype = 'f2'
                return column.name, coltype
            except:
                print(column.name, coltype, coltype.type, type(column))
                raise

        # All values and types
        v = df.values
        types = df.dtypes
        struct_types = [make_col_type(col, types) for col in df.columns]
        dtypes = np.dtype(struct_types)

        # The target empty array
        array = np.zeros(v.shape[0], dtypes)

        # For each type fill in the empty array
        for (i, k) in enumerate(array.dtype.names):
            try:
                if dtypes[i].str.startswith('|S'):
                    array[k] = df[k].str.encode('utf-8').astype('S')
                else:
                    array[k] = v[:, i]
            except:
                raise

        return array, dtypes


