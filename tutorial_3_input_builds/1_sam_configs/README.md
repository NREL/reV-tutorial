System Advisor Model (SAM) Configuration Files
===

The first input you will need to either build or acquire is a SAM system 
configuration file for your target generation technology. This can be done in
multiple ways:
  1) Build a JSON dictionary from scratch using the PySAM documentation page:
      https://nrel-pysam.readthedocs.io/en/latest/index.html.
      - Go to "List of SSC Compute Modules" and click on your target
        technology (e.g., PVWattsv8 for photovolatic systems).
      - Go to the System Design Group and use these key words and descriptions
        to manually piece your system together.
      - For any parameter that you don't want to use the default value for,
        add an entry of your own.
  2) Use the SAM GUI to build a system and then export the parameters to a
      JSON file (that reV can then use).
      - Download SAM's GUI here: https://sam.nrel.gov/download.html
      - Open SAM, start a new project, choose your "performance model",
        then choose the specific SAM module, then choose your financial
        model.
      - Enter your system design parameters for all entries that you don't
        want to use the defaults for (location is not applicable here).
      - Once you're done, go to the title tab for the project (defaults to
        "untitled"), click the dropdown icon ("⌄"), click "generate code",
        and select "JSON for inputs". Click "OK", download the file, then
        edit the file to remove ("solar_resource_file") since that will be
        handled in reV.
      - This becomes your input for "sam_files" in `config_generation.json`.
        