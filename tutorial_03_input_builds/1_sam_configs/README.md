System Advisor Model (SAM) Configuration Files
===

The first input you will need to either build or acquire is a SAM system 
configuration file for your target generation technology. This can be done in
multiple ways:
  1) Build a JSON dictionary from scratch using the 
  [PySAM documentation page](https://nrel-pysam.readthedocs.io/en/latest/index.html):
      - Go to "List of SSC Compute Modules" and click on your target
        technology (e.g., PVWattsv8 for photovoltaic systems).
      - Go to the System Design Group and use these keywords and descriptions
        to manually piece your system together.
      - For any parameter that you don't want to use the default value for,
        add an entry of your own.
  2) Use the SAM GUI to build a system and then export the parameters to a
      JSON file (that reV can then use).
      - Download [SAM's GUI](https://sam.nrel.gov/download.html).
      - Open SAM, start a new project, choose your "performance model",
        then choose the specific SAM module, then choose your financial
        model.
      - Enter your system design parameters for all entries that you don't
        want to use the defaults for (location is not applicable here).
      - Once you're done, go to the title tab for the project (defaults to
        "untitled"), click the dropdown icon ("⌄"), click "generate code",
        and select "JSON for inputs". Click "OK", download the file, then
        edit the file to remove the resource file entry since that will be
        handled in reV.
      - This becomes your input for the `sam_files` entry in the following 
        tutorial's config files. Note that the GUI method will 
        include many entries, including default values and labels, that are 
        not necessary for reV and will not affect the reV CLI runs. 
        Thus, the SAM config file is tailored to minimum entries 
        for reV to run in the following tutorial folders, 
        named `config_SAM.json`. 

<pre>
{
    "array_type": 2, <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.SystemDesign.array_type" target=”_blank” >🔗</a>
    "azimuth": 180, <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.SystemDesign.azimuth">🔗</a>
    "capital_cost": 39767200, <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Lcoefcr.html#PySAM.Lcoefcr.Lcoefcr.SimpleLCOE.capital_cost">🔗</a> 
    "dc_ac_ratio": 1.3, <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.SystemDesign.dc_ac_ratio">🔗</a> 
    "fixed_charge_rate": 0.096, <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Lcoefcr.html#PySAM.Lcoefcr.Lcoefcr.SimpleLCOE.fixed_charge_rate">🔗</a> 
    "fixed_operating_cost": 260000, <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Lcoefcr.html#PySAM.Lcoefcr.Lcoefcr.SimpleLCOE.fixed_operating_cost">🔗</a> 
    "losses": 14.07566, <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.SystemDesign.losses">🔗</a> 
    "module_type": 0, <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv5.html#PySAM.Pvwattsv5.Pvwattsv5.SystemDesign.module_type">🔗</a> 
    "system_capacity": 20000, <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.SystemDesign.system_capacity">🔗</a> 
    "tilt": 0, <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.SystemDesign.tilt">🔗</a> 
    "variable_operating_cost": 0 <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Lcoefcr.html#PySAM.Lcoefcr.Lcoefcr.SimpleLCOE.variable_operating_cost">🔗</a> 
}
</pre>


More On SAM
===
If you want to check other SAM config variables, you can open the SAM's GUI project `*.sam` file, click the "File" dropdown icon ("⌄"), and click "Inputs browser" and it will show the full list of variables from SAM. For further reading on the required input parameters, find the target PySAM module documentation. For example, the most commonly used modules in reV can be found here:

- Solar: [https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html](https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html)
        
- Wind: [https://nrel-pysam.readthedocs.io/en/latest/modules/Windpower.html](https://nrel-pysam.readthedocs.io/en/latest/modules/Windpower.html)
