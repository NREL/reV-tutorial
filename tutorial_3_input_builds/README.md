# Building reV Inputs

For a full model pipeline, as far as input datasets go, reV requires: 

1) A SAM configuration JSON
2) A resource data HDF5 file
3) A project points CSV file
4) An exclusion HDF5 file
5) A transmission connection CSV table

It is actually possible to split the transmission and exclusion data into multiple files, though we'll assume one each for now.
Optionally, there are various points in the model pipeline where you can override constant input parameters with site specific parameters.

In each of these folders, you will find a sample Python script that will generate an input dataset and a README explaining how that script works.
