Project points need to be made before running reV.
These points are taken from the resource data for the technology that is being 
run (NSRDB, WTK)
The example code in this folder is using a subset of the wind toolkit points and
 subsetting them to contain points 
that are only found in Rhode Island.

The project points file must have two columns, anything else is optional:
  1) "gid": The index position of the x-axis of the resource array, or the row index of the resource meta data table.
  2) "config": The key associated with a SAM config in the config_gen.json file. For solar it is 'default' and wind it is 'onshore'.

The points are then used as example inputs to the tutorial_4 and tutorial_5. 
