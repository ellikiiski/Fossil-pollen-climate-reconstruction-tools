## Visualization tools

Python code for creating maps and plots for pollen adn resconstructed temperature data. Good luck, this is not that well documentated sorryy.

#### `prep_pollen_data.py`

Assumes we have a json file of normalized pollen data (from Pollen data tools). That is a big file with all the sites, the pollen data being listed under each. Now we want to get the data under different taxa, sorted under different ages.

INPUT: normalized.json
OUTPUT: ABIES.json etc. files for all taxa

#### `draw_pollen_maps.py`

Assumes we have used the `prep_pollen_data.py` above to generate the json files for each taxon. Now we want to draw six maps for the six age slots, visualizing the prevalence of pollen in sites across Europe.

INPUT: ABIES.json etc. files for all taxa
OUTPUT: ABIES.pdf etc. for all taxa

#### `draw_temperature_reconstructions.py`

Draws maps from the reconstructed temperatures.

#### `draw_plots.py`

Drwas plots for summer and winter temperatures.