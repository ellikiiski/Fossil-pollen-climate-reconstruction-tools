"""
Draw maps from data prepped with prep_pollen_data.py.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import json
import numpy as np
from matplotlib.lines import Line2D

def create_combined_map(taxon, pollen_data, save=False, filename='maps/map.pdf'):
    """Creates 3x2 maps with pollen data. Saves as pdf (if save=True)
    or shows in a new window (if save=False)."""

    # Create a figure with 3 rows and 2 columns for subplots
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(15, 15),
                             subplot_kw={'projection': ccrs.Stereographic(central_longitude=27.75, central_latitude=68.75)})

    # Set the extent and features for each subplot
    for ax in axes.flat:
        ax.set_extent([-10, 60, 40, 75], crs=ccrs.PlateCarree())
        ax.coastlines()
        ax.add_feature(cfeature.BORDERS, edgecolor='#14281D')
        ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='white')
        ax.add_feature(cfeature.OCEAN, facecolor='#DDDBF1')
    
    # Add latitude and longitude gridlines every 10 degrees
        gl = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(), color='gray', linestyle='--', linewidth=0.5)
        gl.xlocator = plt.FixedLocator(np.arange(-15, 61, 15))  # Longitude lines every 10 degrees
        gl.ylocator = plt.FixedLocator(np.arange(30, 76, 15))  # Latitude lines every 10 degrees
        gl.xlabel_style = {'size': 10, 'color': 'gray'}
        gl.ylabel_style = {'size': 10, 'color': 'gray'}

    # List of age periods
    periods = list(pollen_data.keys())
    
    # Plot each map in a subplot
    for i, period in enumerate(periods):
        ax = axes[(5-i) // 2, (5-i) % 2]  # Determine the subplot position (flip the order)
        locations = pollen_data.get(period, {})
        
        for coord, pollen_amount in locations.items():
            lat, lon = map(float, coord.split(", "))

            # Set color based on pollen_amount
            if pollen_amount < 0.33:
                color = '#EFA00B'  # Yellow-ish
            elif 0.33 <= pollen_amount < 0.66:
                color = '#D65108'  # Orange-ish
            else:
                color = '#830A48'  # Red-ish
            
            # Apply square root scaling to pollen_amount to scale circle sizes
            size = np.sqrt(pollen_amount) * 200  # Scale factor to adjust overall sizes
            
            # Plot the scatter points with the scaled size and color
            ax.scatter(lon, lat, s=size, c=color, alpha=0.75, transform=ccrs.PlateCarree(), label=f"{period} BP")

        # Set the title for each subplot
        ax.set_title(f'{get_period_title(period)} BP', fontsize=12)
        ax.label_outer()  # Hide x and y labels for better layout
    
    # Set a main title for the entire figure
    plt.suptitle(f'{taxon} Pollen Map', fontsize=16, y=1.03)

    # Adjust layout with more space on the left and right and reduce space between subplots
    plt.subplots_adjust(left=0.1, right=0.9, top=0.93, bottom=0.07, wspace=0.3, hspace=0.3)

    # Add a legend for all subplots (outside the grid)
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#EFA00B', markersize=10, label='< 0.33 pollen amount'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#D65108', markersize=10, label='0.33 - 0.66 pollen amount'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#830A48', markersize=10, label='> 0.66 pollen amount')
    ]
    
    fig.legend(handles=legend_elements, loc='lower center', ncol=3, fontsize=12, frameon=False)

    # Save or display the combined map
    if save:
        plt.savefig(filename, format='pdf', bbox_inches='tight')
    else:
        plt.show()

def get_period_title(period):

    period = int(period)

    if period == 11500:
        return f'{period}-{period-1500}'
    
    return f'{period}-{period-2000}'


if __name__ == '__main__':

    taxon_data_json_folder = 'data'
    # Split the taxa in multiple group to get shorter runtimes
    taxa1 = [
        "ABIES", "ACER", "AESCULUS", "ALNUS", "APIACEAE", "ARMERIA", "ARTEMISI", 
        "ASTERACE", "BETULA", "BORAGINA", "BRASSICA", "BUXUS", "CAMPANUL", 
        "CAPRIFOL", "CARYOPHY", "CASTANEA", "CHENOPOD", "CORNUS", "CORYLUS", 
    ]
    taxa2 = [
        "CYPERACE", "DRYAS", "ELAEAGNA", "EPHEDRA", "EQUISETU", "ERICACEA", 
        "EUPHORBI", "FABACEAE", "FAGUS", "FRAXINUS", "JUGLANDA", "JUNIPERU", 
        "LAMIACEA", "LARIX", "LILIACEA", "LYCOPODI", "MALVACEA", "MYRICA_G"
    ]
    taxa3 = [ 
        "OLEA", "ONAGRACE", "OSTRYCAR", "PICEA", "PINUS", "PISTACIA", 
        "PLANTAGO", "PLATANUS", "POACEAE", "POLEMONI", "POLYGONA", 
        "POLYPODI", "POPULUS", "PTERIDIU", "QUER_DEC", "QUER_EVE"
    ]
    taxa4 = [
        "RANUNCUL", "RHAMNACE", "ROSACEAE", "RUBIACEA", "RUBUS", 
        "RUMEXOXY", "SALIX", "SANGUISO", "SAXIFRAG", "SCROPHUL", 
        "SELAGINE", "SPHAGNUM", "TAXUS", "THALICTR", "TILIA", 
        "ULMUS_ZE", "URTICACE"
    ]

    # Small taxa set for testing
    taxa_test = ['ABIES']

    for taxon in taxa1: # Change taxa group to desired

        taxon_data_json_file = f'{taxon_data_json_folder}/{taxon}.json'

        try:
            with open(taxon_data_json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)

                create_combined_map(taxon, data, save=True, filename=f'maps/{taxon}_test.pdf')

        except FileNotFoundError:
            print(f"Error: File '{taxon_data_json_file}' not found.")

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in '{taxon_data_json_file}': {e}")
