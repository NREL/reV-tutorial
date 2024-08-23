# -*- coding: utf-8 -*-
"""Create a single set of outputs with PySAM.

Created on Sun Jan 16 10:35:16 2022

@author: travis
"""
import os
import json

import PySAM.Singleowner as so
import PySAM.Windpower as wp


# Sam Config
SINGLE_OWNER = "../../configs/sam/windpower_singleowner_9ws.json"
GEN = "../cli_runs/single_owner/outputs/outputs_gen_2012.h5"


def runit():
    """Run single site model."""
    # Get the configuration
    with open(SINGLE_OWNER, "r") as file:
        config = json.load(file)

    # Initialize a single owner model
    system_model = wp.default("WindPowerSingleOwner")
    financial_model = so.from_existing(system_model, "WindPowerSingleOwner")
    
    
    for k, v in config.items():
        so.value(k, v)
