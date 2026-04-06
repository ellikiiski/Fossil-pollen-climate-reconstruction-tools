import os
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import json
import numpy as np
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

def get_temperature_data(excel_data, max_age_for_avg, min_samples=0):
    for_average = excel_data[excel_data['Age_cal_a'] < max_age_for_avg]

    if len(for_average) < min_samples:
        #print(f'Liian vähän sampleja: {len(for_average)} kpl')
        return None
    
    temps_july = for_average.iloc[:, 1:7]
    temps_january = for_average.iloc[:, 7:13]

    avg_july = temps_july.mean(numeric_only=True).mean()
    avg_january = temps_january.mean(numeric_only=True).mean()
    
    temp_data = {
        'jul_avg': avg_july,
        'jan_avg': avg_january
    }

    periods = [0, 2000, 4000, 6000, 8000, 10000, 11500]
    models = excel_data.columns[1:13]

    temp_data['july_models_mean'] = dict()
    temp_data['july_models_sd'] = dict()
    temp_data["january_models_mean"] = dict()
    temp_data['january_models_sd'] = dict()

    for i in range(len(periods) - 1):
        period_lower = periods[i]
        period_upper = periods[i+1]

        period_data = excel_data[(excel_data['Age_cal_a'] < period_upper) & (excel_data['Age_cal_a'] >= period_lower)]
        
        july_temps = list()
        janu_temps = list()
        for model_name in models:
            temperature = period_data[model_name].mean()
            temp_dif = temperature
            if 'jul' in model_name:
                temp_dif -= avg_july
                july_temps.append(temp_dif)
                #print(july_temps)
            if 'jan' in model_name:
                temp_dif -= avg_january
                janu_temps.append(temp_dif)
                #print(janu_temps)

            if model_name not in temp_data:
                temp_data[model_name] = {}

            temp_data[model_name][period_upper] = {'temperature': temperature,
                                                   'temp_dif': temp_dif}

        july_mean = np.mean(july_temps)
        july_sd = np.std(july_temps)
        janu_mean = np.mean(janu_temps)
        janu_sd = np.std(janu_temps)
        temp_data['july_models_mean'][period_upper] = july_mean
        temp_data['july_models_sd'][period_upper] = july_sd
        temp_data['january_models_mean'][period_upper] = janu_mean
        temp_data["january_models_sd"][period_upper] = janu_sd
        
    return temp_data

def get_location(file_name):
    parts = file_name.split('_')
    name = f'{parts[0]}_{parts[1]}'

    with open('input/normalized.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for site in data:
        if site['filename'] == name:
            return {'latitude': site['latitude'], 'longitude': site['longitude']}
    return None

def empty_north_european_map_plot(rows, cols, coord_lines=False):
    # Create a figure with 3 rows and 2 columns for subplots
    fig, axes = plt.subplots(
        nrows=rows,
        ncols=cols,
        figsize=(15, 15),
        subplot_kw={
            "projection": ccrs.Stereographic(
                central_longitude=27.75, central_latitude=68.75
            )
        },
    )

    # Set the extent and features for each subplot
    for ax in axes.flat:
        ax.set_extent([-10, 60, 40, 75], crs=ccrs.PlateCarree())
        ax.coastlines()
        ax.add_feature(cfeature.BORDERS, edgecolor="#14281D")
        ax.add_feature(cfeature.LAND, edgecolor="black", facecolor="white")
        ax.add_feature(cfeature.OCEAN, facecolor="#D8DBD8")

        if coord_lines:
            gl = ax.gridlines(
                draw_labels=True,
                crs=ccrs.PlateCarree(),
                color="gray",
                linestyle="--",
                linewidth=0.5,
            )
            gl.xlocator = plt.FixedLocator(np.arange(-15, 61, 15))  # Longitude lines
            gl.ylocator = plt.FixedLocator(np.arange(30, 76, 15))  # Latitude lines
            gl.xlabel_style = {"size": 10, "color": "gray"}
            gl.ylabel_style = {"size": 10, "color": "gray"}

    return (fig, axes)

def draw_mean_sd_maps_for_season(folder_path, map_type, season):

    rows = 5
    columns = 1
    fig, axes = empty_north_european_map_plot(rows, columns)

    periods = [4000, 6000, 8000, 10000, 11500]

    if map_type == 'mean':
        cmap = plt.cm.coolwarm
        norm = Normalize(vmin=-5, vmax=5)
        sm = ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
    elif map_type == 'sd':
        cmap = plt.colormaps['magma'].reversed()
        norm = Normalize(vmin=0, vmax=3)
        sm = ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
    else:
        print(f'Not acceptable map type "{map_type}" (must be mean or sd).')
        return None
    
    if season == 'july':
        if map_type == 'mean':
            model = 'july_models_mean'
        if map_type == 'sd':
            model = 'july_models_sd'
    elif season == 'january':
        if map_type == 'mean':
            model = 'january_models_mean'
        if map_type == 'sd':
            model = 'january_models_sd'
    else:
        print(f'Not acceptable season "{season}" (must be july or january).')
        return None

    discard_count = 0
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)

        try:
            data = pd.read_excel(file_path)
            temp_data = get_temperature_data(data, 2000, 3)

            if temp_data:
                location = get_location(file)
                lat = location["latitude"]
                lon = location["longitude"]

                # Plot each map in a subplot
                for i, period in enumerate(periods):
                    ax = axes[(len(periods)-1-i)]  # Determine the subplot position

                    #print(temp_data[model_name])
                    temperature = temp_data[model][period]

                    # Plot the scatter points with the scaled size and color
                    ax.scatter(
                        lon,
                        lat,
                        s=25,
                        c=[temperature],
                        cmap=cmap,
                        norm=norm,
                        alpha=0.75,
                        transform=ccrs.PlateCarree(),
                    )

                    # Set the title for each map
                    ax.set_title(f"{get_period_title(period)} BP", fontsize=12)
            else:
                discard_count += 1

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")

        
    # Add colorbar for the gradient scale below all maps
    cbar_ax = fig.add_axes([0.15, 0.04, 0.7, 0.02])  # [left, bottom, width, height]
    cbar = fig.colorbar(sm, cax=cbar_ax, orientation="horizontal")
    cbar.set_label("Temperature Difference (°C)", fontsize=12)

    # Adjust layout to leave room for the colorbar
    plt.subplots_adjust(left=0.1, right=0.9, top=0.93, bottom=0.1, wspace=0.3, hspace=0.3)

    # Set a main title for the entire figure
    plt.suptitle(f'{season.upper()} {map_type.upper()}', fontsize=16, y=0.98)

    print(f'Heitettiin roskiin {discard_count} saittia.')

    print("Tallennetaan...")
    plt.savefig(f"{season}_{map_type}.pdf", format="pdf", bbox_inches="tight")
    print(f'{season}_{map_type}.pdf tallennettu!')




def draw_six_maps_for_model(folder_path, model_name):

    rows = 3
    columns = 2
    fig, axes = empty_north_european_map_plot(rows, columns, coord_lines=True)

    # List of age periods
    periods = [2000, 4000, 6000, 8000, 10000, 11500]

    # Choose a color map
    cmap = plt.cm.coolwarm  # You can choose another color map like 'viridis', 'plasma', etc.
    norm = Normalize(vmin=-5, vmax=5)  # Set the range for color normalization (-5 to 5)

    # Create a ScalarMappable object for mapping temperature values to colors
    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # Just to make the ScalarMappable work

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)

        try:
            data = pd.read_excel(file_path)
            temp_data = get_temperature_data(data, 2000, 3)

            if temp_data:
                location = get_location(file)
                lat = location["latitude"]
                lon = location["longitude"]

                # Plot each map in a subplot
                for i, period in enumerate(periods):
                    ax = axes[(len(periods)-1-i) // columns, (len(periods)-1-i) % columns]  # Determine the subplot position

                    #print(temp_data[model_name])
                    temperature = temp_data[model_name][period]["temp_dif"]

                    # Plot the scatter points with the scaled size and color
                    ax.scatter(
                        lon,
                        lat,
                        s=25,
                        c=[temperature],
                        cmap=cmap,
                        norm=norm,
                        alpha=0.75,
                        transform=ccrs.PlateCarree(),
                    )

                    # Set the title for each map
                    ax.set_title(f"{get_period_title(period)} BP", fontsize=12)

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")

    # Add colorbar for the gradient scale below all maps
    cbar_ax = fig.add_axes([0.15, 0.04, 0.7, 0.02])  # [left, bottom, width, height]
    cbar = fig.colorbar(sm, cax=cbar_ax, orientation="horizontal")
    cbar.set_label("Temperature Difference (°C)", fontsize=12)

    # Adjust layout to leave room for the colorbar
    plt.subplots_adjust(left=0.1, right=0.9, top=0.93, bottom=0.1, wspace=0.3, hspace=0.3)

    # Set a main title for the entire figure
    plt.suptitle(f"{model_name}: Temperature Map", fontsize=16, y=0.98)

    print("Tallennetaan...")
    plt.savefig(f"{model_name}.pdf", format="pdf", bbox_inches="tight")


def get_period_title(period):
    period = int(period)
    if period == 11500:
        return f'{period}-{period-1500}'
    return f'{period}-{period-2000}'

if __name__ == '__main__':
    folder_path = 'temperatures'
    models = [
    "WA_Tjul", "WAPLS_Tjul", "MAT_Tjul", "RF_Tjul", "ERT_Tjul", "BRT_Tjul",
    "WA_Tjan", "WAPLS_Tjan", "MAT_Tjan", "RF_Tjan", "ERT_Tjan", "BRT_Tjan"
    ]
    map_types = ['mean', 'sd']
    seasons = ['july', 'january']

    #draw_six_maps_for_model(folder_path, model, 5, 2)
    start_time = time.time()
    for map_type in map_types:
        for season in seasons:
            print(f'Toimitetaan {season} {map_type}...')
            draw_mean_sd_maps_for_season(folder_path, map_type, season)
    end_time = time.time()
    duration = end_time - start_time
    print(f'Time taken: {duration:.6f} sec')
