System Advisor Model (SAM) Configuration Files
===

## The System Advisor Model

SAM is an open-source and free application that simulates performance and economics for a suite of energy technologies. It serves as the core of reV's generation modules. The actual SAM simulation code can be found in the SAM Simulation Core (https://github.com/NREL/ssc), which a library of C and C++ code. This code is accessed through reV via the PySAM Python package (https://github.com/NREL/pysam), which is a wrapper for the lower-level C code in the simulation core and is how reV calls SAM.

You can think of reV, at least for the initial generation modules in any reV modeling pipeling, as a spatial coordinator of SAM. The reV model allows you to (relatively) easily run SAM models at every location in a study area. You can use it to simulate a singular technology across the full extent of a study area or to run different technologies or system designs at specified locations in that study area. Regardless of how you intend to use reV, at least one SAM configuration file will be required for any reV run.

So, we need a way to communicate SAM parameters to reV. This is done via JSON configuration files, which are basically dictionaries as files. reV can take in JSON or JSON5 (which allows comments) formatted files. So, the first input you will need is a SAM configuration file in JSON format for your target generation technology or technologies. 

SAM is a *very* extensive and detailed model. It can model many different technologies and, within each, there are countless parameters that can be set. A thorough understanding of SAM (and how to specify a SAM configuration file to a particular energy generator) requires significant study and practice with the model. This tutorial will not attempt to replace existing SAM tutorials, instead its goal is simply to demonstrate how to create a configuration file that will integrate with reV. For more resources for learning about SAM and how to use it, please visit:

  - The SAM website: https://sam.nrel.gov/
  - The SAM YouTube Page: https://www.youtube.com/channel/UC_Z7m8z5tOclfNgaTfGDdPQ
  - The SAM  user forum: https://sam.nrel.gov/forum.html

## Building a configuration file
Building a SAM configuration file can be done in two main ways:
  1) Build a JSON dictionary from scratch using the 
  [PySAM documentation page](https://nrel-pysam.readthedocs.io/en/latest/index.html):
      - Go to "List of SSC Compute Modules" and click on your target
        technology (e.g., PVWattsv8 for photovoltaic systems).
      - Go to the "System Design Group" and use these keywords and descriptions
        to manually piece your system together.
      - For any parameter that you don't want to use the default value for,
        add an entry of your own.
      - You can use Python and the `json` package to write these parameters to a JSON-compliant file, or you may write these parameters directly to a file as long as you follow the formatting rules. Here is JSON's website for a direct reference to these formatting criteria: https://www.json.org. Basically, use Python's dictionary format, but avoid trailing commas (unless you're using JSON5).
  
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
        named `config_SAM.json`

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


Examples
===
The two most commonly used SAM modules used in reV can be found here:

- Solar: [https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html](https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html)

- Wind: [https://nrel-pysam.readthedocs.io/en/latest/modules/Windpower.html](https://nrel-pysam.readthedocs.io/en/latest/modules/Windpower.html)
