## Tools for fossil pollen based climate reconstructions

In this repository, you find the data and scripts used in my Master's thesis \[insert name here\] (2026) from the University of Helsinki. The thesis itself is available \[insert link info here\]. In the study we reconstructed the Holocene climate in northern Europe using fossil pollen data as a proxy.

### Data and output

The fossil pollen data gathered from 211 sites in northern Europe and the reconstructed temperature predictions for those sites can be found in the folder Data and output.

#### Harmonized fossil pollen data

The pollen data and the metadata of the sites:
- Harmonized fossil pollen data (csv file)
- Metadata of the fossil pollen sites (csv file)

#### Reconstructed temperature values

The output of the climate reconstruciton models:
- Reconstructed temperature predictions per model (csv file)

### Code

*DISCLAIMER*: The code here is written during summer 2024 has not been kept up to date. Also, the level of documentation and clarity of the code varies.

#### Pollen data tools (pollen data processing)

Gathering and standardizing the fossil pollen data to be compatible with the climate reconstruction models.

- Fetch fossil pollen data from Neotoma database
- Filter the data based on chose criteria
- Harmonize the the data under given labels

#### Visualization tools (maps and plots)

Both the fossil pollen data and temperatures from the climate reconstruction visualized in various ways.

- Fossil pollen site maps
- Paleotemperature maps of the reconstructions
- Peleotemperature plots per reconstruciton model

#### PCA tools (principal component analysis)

The patterns in pollen data are visualized with PCA with CLR trnsformation.

- Explained variance of the first 5 components
- First two PCs visualized
