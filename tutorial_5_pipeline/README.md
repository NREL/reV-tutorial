reV pipeline
===========================

This tutorial introduces how to execute multiple reV steps in one single analysis pipeline. We included the config files from the `generation` and `multi-year` module in `tutorial_4_generation_a` and `_b`, with a QA/QC config file that perfoms quality assurance checks on reV output data. To successfully run a reV pipeline, one and only one file with "pipeline" in the name should exist in this directory and contain the config information. `config_pipeline.json` is made with a list of dictionaries where each of them represents one step in the pipeline:

```json
    "pipeline": [
      {
        "generation": "./config_gen.json"
      },
      {
        "multi-year": "./config_multi-year.json"
      },
      {
        "qa-qc": "./config_qa-qc.json"
      }
    ]
```

Then, for the `multi-year` module, instead of set an explicit list of file names for the entry `source_files`, we set this entry to "PIPELINE" so that the input is determined from the status file of the previous pipeline step: 

```json
"source_files": "PIPELINE",
```

Simply run the following command to execute the pipeline run: 

```
reV pipeline -c config_pipeline.json --monitor
```

The `--monitor` flag allows a continuous monitoring of the pipeline run with messages pop up in terminal. 
