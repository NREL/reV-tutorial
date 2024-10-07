reV pipeline
===========================

This tutorial introduces how to execute multiple reV steps in one single analysis pipeline. We included the config files from the `generation` and `multi-year` module in `tutorial_4_generation_a` and `_b`. To successfully run a reV pipeline, one and only one file with "pipeline" in the name should exist in this directory and contain the config information. `config_pipeline.json` is made with a list of dictionaries where each of them represents one step in the pipeline:

```json
    "pipeline": [
      {
        "generation": "./config_gen.json"
      },
      {
        "multi-year": "./config_multi-year.json"
      }
    ]
```

Then, for the `multi-year` module, instead of set an explicit list of file names for the entry `source_files` in the `config_multi-year.json` file like we did in [tutorial_4_generation_a](../tutorial_4_generation_b/config_multi-year.json), we set this entry to "PIPELINE" so that the input for the `multi-year` module is determined automatically from the status file of the previous pipeline step: 

  ```json
    "groups": {
    "none": {
        "source_files": "PIPELINE",
      }
    }
  ```

Other entries used in the config files are the same as in `tutorial_4_generation_a/b`. After setting up the configs, simply run the following command to execute the pipeline run: 

```
reV pipeline -c config_pipeline.json --monitor
```

The `--monitor` flag allows a continuous monitoring of the pipeline run with messages pop up in terminal. 
