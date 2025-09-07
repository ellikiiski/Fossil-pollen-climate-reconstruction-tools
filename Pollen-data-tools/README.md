## Fossil pollen data processing

The Pollen-data-tools package contains the pipeline to 1) fetch, 2) filter and 3) harmonize fossil pollen data from Neotoma database to be input to the climate reconstruction models of Salonen et al. (2019).

Contents
- Purpose
- Workflow
- User guide

### Purpose

...

### Workflow

\[Picture coming...\]

#### 1) Data fetching

Neotoma database offers the possibility to fetch sites through the API. However, to get the full radiocarbon dated fossil pollen datasets from desired region requires multiple steps.

##### A) Metadata

First, we retrieve the metadata of all sites that have data of both 'pollen' and 'geochronologic' types. At this point, also the location of the site is compared to the desired region, and only those inside of it saved.

##### B) Datasets

Next, we make a new API request for all the sites saved in the metadata fetching to get the actual pollen samples and radiocarbon datings.

#### 2) Data filtering

The location filtering was already done in metadata fetching to reduce the number of sites as early as possible. Now, with the full datasets, we can drop out more inadequate sites. The conditions for the following filters provided by the program can be specified in the file `parameters.py`.

Filters
- Location (filtered already in metadata fetching)
- Age range to be covered by the pollen samples
- Minumum number of pollen samples
- Minimum number of radiocarbon datings

#### 3) Data harmonizing

...

### User guide