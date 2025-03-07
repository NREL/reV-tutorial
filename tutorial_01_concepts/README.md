# Outline for a video tutorial series - Episode #1 (Under Construction)
### The goals of this tutorial: 
- Get you familiarized with the idea of renewable energy potentials and their assessments
- Develop fundamental understanding of technical potential and reV (renewable energy potential) model

### Geospatial Data Science – Who we are, what we do?
NREL's geospatial data science research uses geographic information systems (GIS) to produce maps, analyses, models, applications, and visualizations that inform energy planning and production. The tutorial series are led by:  
- Travis Williams, Researcher – III, GDS group
- Chinna Subbaraya Siddharth (Sid) Ramavajjala, Researcher - II, GDS group 

### Renewables Vs. Non-renewables
We’ll try to understand how energy assessments happen across energy spectrum – renewables vs. oil & gas. Therefore, how to define resource potential is important. The energy generator has to be in the same place where there is resource availability. Therefore, understanding where the resource is available and how much is it available bring is the starting point to any kind of energy analysis.

What is a resource?
- Resource is the input utilized for energy generation (electricity) by a generator (Wind Turbine, Solar Panel, Steam Turbine etc.)
Renewable energy is a site-specific resource and cannot be transported elsewhere for energy generation. Non-renewables like Crude oil, Natural gas, Coal are not site-specific resources, and they can be transported to a generation site.

![re_potential_cirlces_diagram](https://github.com/user-attachments/assets/ae2aff1c-6117-4977-8f7f-a686a147b6a7)
*Renewable Energy Assessments - Levels of Potential.*
*Source: Geospatial Data Science Group - National Renewable Energy Laboratory (2024).* 
 <!-- [Reference or URL](https://example.com) -->

### Resource Potential
The resource potential is the theoretical availability of renewable energy across an area is resource potential. It quantifies the energy content of a resource at specific location. There are two resource datasets developed at NREL for understanding solar resource potential and wind resource potential:
- National Solar Radiation Database (NSRDB) for solar (Sengupta et al. 2018)
![nsrdb_coverage_map_042024](https://github.com/user-attachments/assets/a3b7778d-b126-46ef-91d1-73a2447aa216)
*Source: Geospatial Data Science Group - National Renewable Energy Laboratory (2024).* 

- Wind Integrated National Dataset Toolkit (WTK) for wind (Draxl et al. 2015)
![wtk_coverage_map_042024](https://github.com/user-attachments/assets/302cf3e2-aaf4-407d-8172-a175ec0e6c60)
*Source: Geospatial Data Science Group - National Renewable Energy Laboratory (2024).* 


### Introducing the reV Model and Defining Technical Potential
- The idea of technical potential
    - Define tech pot (reV 2019 & reV 2023 reports).
        - Technical potential is a measure of resource potential (i.e., capacity) that could be developed based on assumptions of the developable land area defined by the user; in other words, how much renewable energy capacity could be developed in a given land area after accounting for land exclusions predefined by the user. 
        - For example, the user can limit development by land ownership, terrain, land use/cover, and urban areas, as well as other custom inputs.
        
    - Contextualize in terms of broader energy availability assessment (e.g., geological surveys in the Oil and Gas industry; https://www.eia.gov/todayinenergy/detail.php?id=17151)
        - Geological surveys are conducted in the oil and gas industries to assess the available total resources underground, which is referred to the in-place resources. The tech pot in renewable energy has a similar definition to the in-place resources in the oil and gas industry, where we are measuring the maximum available energy or resources after applying exclusions and contraints. 

    - Ideally, we'll convince Galen or Donna or Anthony to make a guest appearance and describe their thought process when they developed the technical potential analysis approach...this could also lead directly into the Model

- One of the main responsibility of GDS is the renewable energy potential a.k.a reV model. What is it? 
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

Oil and Gas Energy Assessments - Levels of Potential 
![oil_gas_potential_cirlces_diagram](https://github.com/user-attachments/assets/8c1592e6-5a45-4c3e-a254-e6e59e01ab71)
Source: U.S. Energy Information Administration (2014). https://www.eia.gov/todayinenergy/detail.php?id=17151.

NREL Modeling Ecosystem
![seac_ecosystem](https://github.com/user-attachments/assets/74ceb6cc-9b2f-463a-84cf-873abe6f673e)



