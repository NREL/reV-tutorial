Advanced Input Building
===
- Least-cost Transmission
- Custom Resource Files


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


