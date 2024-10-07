# Outline for a video tutorial series - Episode #1

## Introducing the reV Model and Defining Technical Potential
- Introduce ourselves, who we are, where we work, and what we do
- One of the main responsibility of GDS is the reV model, which is why you're here, etc.
- Before talk about the model, we need introduce the idea of technical potential
    - Define tech pot (reV 2019 & reV 2023 reports).
        - Technical potential is a measure of resource potential (i.e., capacity) that could be developed based on assumptions of the developable land area defined by the user; in other words, how much renewable energy capacity could be developed in a given land area after accounting for land exclusions predefined by the user. 
        - For example, the user can limit development by land ownership, terrain, land use/cover, and urban areas, as well as other custom inputs.
        
    - Contextualize in terms of broader energy availability assessment (e.g., geological surveys in the Oil and Gas industry; https://www.eia.gov/todayinenergy/detail.php?id=17151)
        - Geological surveys are conducted in the oil and gas industries to assess the available total resources underground, which is referred to the in-place resources. The tech pot in renewable energy has a similar definition to the in-place resources in the oil and gas industry, where we are measuring the maximum available energy or resources after applying exclusions and contraints. 

    - Ideally, we'll convince Galen or Donna or Anthony to make a guest appearance and describe their thought process when they developed the technical potential analysis approach...this could also lead directly into the Model

- Introduce the reV model
    - Background info about reV
        - Why it's called reV? It's a short for The Renewable Energy Potential (reV)
        - reV is an open-source geospatial platform for assessing system performance, available capacity, distance to transmission, and total costs for potential solar and wind energy deployment at regional to continental scales.
        - Potential and intended users of reV model outputs include utility planners, regional and national agencies, project and land developers, internal NREL modelers, and external researchers. 
    
    - We might need to add here about the overview of the input-output pipeline of reV, as illustrated in the reV-tutorial repo README? 

    - How speciifcally does the model represent technical potential (e.g., what are the outputs.)
        - The LCOE output can serve as the end point of a reV analysis, providing insight into economic competitiveness, relative performance competitiveness, and regional differences driven by cost assumptions. LCOE estimates can also be used downstream in the supply curves. 
        - The tech pot is represented as a function of the available land area after applying exclusions, the net capacity factor estimated by the generation module, and a user-defined power density appropriate for the specific technology. The power density value represents the maximum potential capacity for a given unit of area (e.g., MW/km2). 

    - How does this model fit into the broader energy modeling ecosystem at NREL.

    - Describe the open-source nature of reV...anyone can use it, though challenges exists in acquiring and/or building input datasets, which we'll cover in Episode #3.
    - Describe who all is using it.

- Renewable energy glossary
    - Abbreviations, concepts, knowledge gaps that might not be familiar to the audiences; we can expand this glossary along the tutorial making process. 
    - SAM = Systems Advisor Model. SAM is an open-source techno-economic software model that simulates estimating power generation and financial viability for renewable energy technologies...(https://sam.nrel.gov).
    - LCOE = Levelized Cost of Energy. LCOE represents the average revenue per unit of electricity generated that would be required to recover the costs of building and operating a generating plant during an assumed financial life. 
    - Supply curves = represent the cost and amount of energy at all reV-modeled potential sites at a snapshot in time. 

- Preview the next episode.
    - Tell the viewers that we'll start setting up the model in the next episode
 

## Images to be assimilated

Resource Data - National Solar Radiation Database
![nsrdb_coverage_map_042024](https://github.com/user-attachments/assets/a3b7778d-b126-46ef-91d1-73a2447aa216)


Resource Data - National Wind Database
![wtk_coverage_map_042024](https://github.com/user-attachments/assets/302cf3e2-aaf4-407d-8172-a175ec0e6c60)


Renewable Energy Assessments - Levels of Potential
![re_potential_cirlces_diagram](https://github.com/user-attachments/assets/ae2aff1c-6117-4977-8f7f-a686a147b6a7)

Source: Geospatial Data Science Group - National Renewable Energy Laboratory (2024). 


Oil and Gas Energy Assessments - Levels of Potential 
![oil_gas_potential_cirlces_diagram](https://github.com/user-attachments/assets/8c1592e6-5a45-4c3e-a254-e6e59e01ab71)

Source: U.S. Energy Information Administration (2014). https://www.eia.gov/todayinenergy/detail.php?id=17151.


NREL Modeling Ecosystem
![seac_ecosystem](https://github.com/user-attachments/assets/74ceb6cc-9b2f-463a-84cf-873abe6f673e)



