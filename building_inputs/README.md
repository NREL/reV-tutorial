# Building reV Inputs

For a full model pipeline, as far as input datasets go, reV requires a resource data HDF5 file, a project points CSV file, a SAM configuration JSON, an exclusion HDF5 file, and a transmission connection CSV table. It is actually possible to split the transmission and exclusion data into multiple files, though we'll assume one each for now.

Optionally, there are various points in the model pipeline where you can override constant input parameters with site specific parameters.

In each of these folders, you will find a sample Python script that will generate an input dataset and a README explaining how that script works.
