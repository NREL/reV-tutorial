# -*- coding: utf-8 -*-
"""Set paths for configs.

Created on Sun Jan 16 13:12:19 2022

@author: travis
"""
import json
import os


# Needed paths
HERE = __file__
HOME = os.path.abspath(os.path.join(HERE, "../../.."))
RESOURCE = os.path.join(HOME, "data/ri_100_wtk_{}.h5")
SAM = os.path.join(HOME, "configs/sam/windpower_singleowner_9ws.json")

# TEMPLATES
GEN_CONFIG = {
  "analysis_years": [
    2012
  ],
  "directories": {
    "log_directory": "./outputs/logs/",
    "output_directory": "./outputs"
  },
  "execution_control": {
    "memory_utilization_limit": 0.9,
    "nodes": 1,
    "sites_per_worker": 20
  },
  "log_level": "INFO",
  "output_request": [
    "cf_mean",
    "cf_profile",
    "ws_mean"
  ],
  "project_points": "./project_points.csv",
  "resource_file": "PLACEHOLDER",
  "sam_files": {
    "wind": "PLACEHOLDER"
  },
  "technology": "windpower"
}
ECON_CONFIG = {
    "analysis_years": [
        2012
    ],
    "cf_file": "outputs/outputs_gen_2012.h5",
    "directories": {
        "log_directory": "./outputs/logs",
        "output_directory": "./outputs"
    },
    "execution_control": {
        "memory_utilization_limit": 0.9,
        "nodes": 1,
        "sites_per_worker": 20
    },
    "log_level": "INFO",
    "output_request": [
        "ppa_price",
        "lcoe_nom",
        "lcoe_real",
        "capital_cost",
        "project_return_aftertax_npv",
        "flip_actual_irr"
    ],
    "technology": "windpower",
    "project_points": "./project_points.csv",
    "sam_files": {
        "wind": "../../configs/sam/windpower_singleowner_8ws.json"

    }
}


def build_configs():
    """reV doesn't like the '..' notation for relative paths."""
    # Generation
    config = GEN_CONFIG.copy()
    config["resource_file"] = RESOURCE
    config["sam_files"]["wind"] = SAM
    with open("config_gen.json", "w") as file:
        file.write(json.dumps(config, indent=4))

    # Econ
    config = ECON_CONFIG.copy()
    config["sam_files"]["wind"] = SAM
    config["output_request"] = [
        "ppa_price",
        "lcoe_nom",
        "lcoe_real",
        "cf_pretax_cashflow",
        "project_return_aftertax_npv",
        "flip_actual_irr"
    ]
    with open("config_econ.json", "w") as file:
        file.write(json.dumps(config, indent=4))


if __name__ == "__main__":
    build_configs()
