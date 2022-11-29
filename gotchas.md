## A List of Common Problems When Configuring and Running reV

### 1) Unneeded commas in the json configuration
    {
        "this": [
            "will",
            "not",
            "work",  # Because of this comma
        ]
    }
    
### 2) SAM config parameter name spelling

    "fixed_operating_costs": 1404000.0,  # This extra "s" on "_costs" caused an hour of confusion
    "fixed_charge_rate": 0.051,
    "system_capacity": 18000,


## 3) Percentage units

    {
      "array_type": 2,
      "azimuth": 180,
      "capital_cost": 39767200,
      "clearsky": false,
      "dc_ac_ratio": 1.3,
      "fixed_charge_rate": 0.096,       # This is 9.6%
      "fixed_operating_cost": 260000,
      "gcr": 0.4,                       # This is 40%
      "inv_eff": 96,                    # This is 96% 
      "losses": 14.07566,               # And this is 14.08%
      "module_type": 0,
      "system_capacity": 20000,
      "tilt": 0,
      "variable_operating_cost": 0
    }


## 4) Tilt parameter with tracking for solar
    {
      "array_type": 2,                  # This refers to 1-axis tracking
      "azimuth": 180,
      "capital_cost": 39767200,
      "clearsky": false,
      "dc_ac_ratio": 1.3,
      "fixed_charge_rate": 0.096,
      "fixed_operating_cost": 260000,
      "gcr": 0.4,
      "inv_eff": 96, 
      "losses": 14.07566,
      "module_type": 0,
      "system_capacity": 20000,
      "tilt": 0,                        # Tracking has no single tilt value, set to 0
      "variable_operating_cost": 0
    }
