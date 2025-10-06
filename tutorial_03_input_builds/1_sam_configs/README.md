System Advisor Model (SAM) Configuration Files
===

## The System Advisor Model

SAM is an open-source and free application that simulates performance and economics for a suite of energy technologies. It serves as the core of reV's generation modules. The actual SAM simulation code can be found in the SAM Simulation Core (https://github.com/NREL/ssc), which a library of C and C++ code. This code is accessed through reV via the PySAM Python package (https://github.com/NREL/pysam), which is a wrapper for the lower-level C code in the simulation core and is how reV calls SAM.

You can think of reV, at least for the initial generation modules in any reV modeling pipeline, as a spatial coordinator of SAM. The reV model allows you to run SAM models at every location in a study area or adjust SAM parameters with site specific parameters. You can use it to simulate a singular technology across the full extent of a study area or to run different technologies and system designs at specified locations or regions. Regardless of how you intend to use reV, at least one SAM configuration file will be required for any reV run.

We need a way to communicate SAM parameters to reV. This is done via JSON configuration files, which allows us to store dictionaries of model parameters on a file system. reV can take in JSON or JSON5 (which allows comments) formatted files. So, the first input you will need is a SAM configuration file in JSON format for your target generation technology or technologies. 

SAM is a *very* extensive and detailed model. It can model many different technologies and, within each, there are countless parameters that can be set. A thorough understanding of SAM (and how to specify a SAM configuration file to a particular energy generator) requires significant study and practice with the model. This tutorial will not attempt to replace existing SAM tutorials. Instead, its goal is simply to demonstrate how to create a configuration file that will integrate with reV. For more resources for learning about SAM and how to use it, please visit:

  - The SAM website: https://sam.nrel.gov/
  - The SAM YouTube Page: https://www.youtube.com/channel/UC_Z7m8z5tOclfNgaTfGDdPQ
  - The SAM  user forum: https://sam.nrel.gov/forum.html

## Building a configuration file
Building a SAM configuration file can be done in several ways, here's a few:

  1) Use the SAM GUI to build a system and then export the parameters to a JSON file (that reV can then use). This is probably the easiest, most foolproof method, and is what is recommended by PySAM for building its own model inputs.
      - Download the SAM GUI: https://sam.nrel.gov/download.html.
      - Open SAM, start a new project, choose your "performance model", then choose the specific SAM module, then choose your financial model.
      - Enter your system design parameters for all entries that you don't want to use the defaults for.
      - Once you're done, go to the title tab for the project (defaults to "untitled"), click the dropdown icon ("⌄"), click "generate code", and select "JSON for inputs". Click "OK", download the file, then        edit the file to remove the resource file entry since that will be handled in reV.
      - This becomes your input for the `sam_files` entry in the following tutorial's config files. Note that the GUI method will include many entries, including default values and labels, that are not necessary for reV and will not affect the reV CLI runs.

  3) Build a JSON dictionary from scratch using the [PySAM documentation page](https://nrel-pysam.readthedocs.io/en/latest/index.html). If you prefer not to (or can't for some reason) download the SAM GUI, you can use the PySAM documentation for a the names, valid values, and descriptions of each input parameter. This may also be useful for small edits to existing SAM JSON configuration files since it's much quicker than building a new system in the GUI.
      - Go to "List of SSC Compute Modules" and click on your target technology (e.g., PVWattsv8 for photovoltaic systems).
      - Go to the "System Design Group" and use these keywords and descriptions to manually piece your system together.
      - For any parameter that you don't want to use the default value for, add an entry of your own.
      - You can use Python and the `json` package to write these parameters to a JSON-compliant file, or you may write these parameters directly to a file as long as you follow the formatting rules. Here is JSON's website for a direct reference to these formatting criteria: https://www.json.org. Probably the main gotcha here is to avoid trailing commas (unless you're using JSON5).


## Example SAM Configuration

The following is a configuration example with the minimum parameters for a PV system and LCOE calculator. Each parameter has a link to its entry in the PySAM documentation and will describe the parameter, provide input options, and give you the default value.

<pre>
{
    <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.SystemDesignarray_type" style="border-bottom: 0px">"array_type"</a>: 2,
    <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.SystemDesign.azimuth">"azimuth"</a>: 180,
    <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Lcoefcr.html#PySAM.Lcoefcr.Lcoefcr.SimpleLCOE.capital_cost">"capital_cost"</a>: 39767200,
    <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.SystemDesign.dc_ac_ratio">"dc_ac_ratio"</a>: 1.3, 
    <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Lcoefcr.html#PySAM.Lcoefcr.Lcoefcr.SimpleLCOE.fixed_charge_rate">"fixed_charge_rate"</a>: 0.096, 
    <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Lcoefcr.html#PySAM.Lcoefcr.Lcoefcr.SimpleLCOE.fixed_operating_cost">"fixed_operating_cost"</a>: 260000, 
    <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.SystemDesign.losses">"losses"</a>: 14.07566, 
    <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv5.html#PySAM.Pvwattsv8.Pvwattsv8.SystemDesign.module_type">"module_type"</a>: 0, 
    <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.SystemDesign.system_capacity">"system_capacity"</a>: 20000, 
    <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html#PySAM.Pvwattsv8.Pvwattsv8.SystemDesign.tilt">"tilt"</a>: 0,
    <a href="https://nrel-pysam.readthedocs.io/en/latest/modules/Lcoefcr.html#PySAM.Lcoefcr.Lcoefcr.SimpleLCOE.variable_operating_cost">"variable_operating_cost"</a>: 0 
}
</pre>

## Editing a JSON file in Python

It can be useful to either automate SAM configuration creation or to use Python to quickly adjust parameters (perhaps not for single value entries, but certainly for larger ones). The block below shows you how to read in a configuration file, adjust values, and write back to file.

```Python
# Import Python's builtin JSON package
import json

# Read the file in as a Python dictionary
config = json.load(open("/path/to/sam_config.json")

# Adjust
config["entry"] = "value"
del config["other_entry"]

# Write the file back to file
with open("/path/to/sam_config.json", "w") as file:
  file.write(json.dumps(config, indent=4))  # Indent for legibility
```


Common Modules
===
Three commonly used SAM modules in reV can be found here:

- Solar (simple): [https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html](https://nrel-pysam.readthedocs.io/en/latest/modules/Pvwattsv8.html)

- Solar (detailed): [https://nrel-pysam.readthedocs.io/en/main/modules/Pvsamv1.html](https://nrel-pysam.readthedocs.io/en/main/modules/Pvsamv1.html)

- Wind: [https://nrel-pysam.readthedocs.io/en/latest/modules/Windpower.html](https://nrel-pysam.readthedocs.io/en/latest/modules/Windpower.html)
