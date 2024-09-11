# Generation Module
This tutorial focuses on the **generation** module of the NREL reV model. 
When running reV, a series of json files are used to inform the model on what configs you want to use.
Throughout the pipeline there are configs that are required and ones that are optional.
All of the steps in the pipeline require execution control.

First, navigate to the `generation` subfolder and run a simple example of generation command. 
This subfolder includes a **configuration JSON** file (`config_gen.json`) that specify the simulation parameters, including system specifications, time periods, output requests, etc.

Next, navigate to the `pipeline` subfolder and run an example command that first combines generation data from multiple years (outputs generated in the `generation` folder) into a single multi-year file, and then conducts a QA/QC that performs quality assurance checks on the `reV` pipeline outputs. 
