System Advisor Model (SAM) Configuration Files
===

The first input you will need to either build or acquire is a SAM system 
configuration file for your target generation technology. This can be done in
multiple ways:
  1) Build a JSON dictionary from scratch using the PySAM documentation page:
      https://nrel-pysam.readthedocs.io/en/latest/index.html.
      - Go to "List of SSC Compute Modules" and click on your target
        technology (e.g., PVWattsv8 for photovoltaic systems).
      - Go to the System Design Group and use these keywords and descriptions
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
      - This becomes your input for the `sam_files` entry in the following 
        tutorials' config files. Note that the GUI method will 
        include many more entries, including default values and labels that are 
        not necessary for reV and will not affect the reV CLI runs. 
        Thus, the SAM config file is tailored to minimum entries 
        for reV to run in the following tutorial folders, 
        named `config_SAM.json`. 

<pre>
{
    "adjust:constant": 0,
    "array_type": 2,
    "azimuth": 180,
    "capital_cost": 39767200,
    "clearsky": false,
    "dc_ac_ratio": 1.3,
    "fixed_charge_rate": 0.096,
    "fixed_operating_cost": 260000,
    "gcr": 0.4,
    "inv_eff": 96, <a class="headerlink" href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.Outputs.inverter_efficiency" target="_blank" >link</a>
    "losses": 14.07566,
    "module_type": 0,
    "system_capacity": 20000,
    "tilt": 0,
    "variable_operating_cost": 0
  }
</pre>








More On SAM
===
Further reading can be done on the specifics of the SAM configs.

- Solar: [https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html](https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html)
        
- Wind: [https://nrel-pysam.readthedocs.io/en/latest/modules/Windpower.html](https://nrel-pysam.readthedocs.io/en/latest/modules/Windpower.html)
