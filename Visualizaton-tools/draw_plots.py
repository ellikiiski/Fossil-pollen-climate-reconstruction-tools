import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from loess.loess_1d import loess_1d


def get_avg_temp(excel_data, max_age_for_avg, min_samples=0):
    for_average = excel_data[excel_data['Age_cal_a'] < max_age_for_avg]

    if len(for_average) < min_samples:
        print(f'Liian vähän sampleja: {len(for_average)} kpl')
        return None
    
    temps_july = for_average.iloc[:, 1:7]
    temps_january = for_average.iloc[:, 7:13]

    avg_july = temps_july.mean(numeric_only=True).mean()
    avg_january = temps_january.mean(numeric_only=True).mean()
    
    temp_data = {
        'jul_avg': avg_july,
        'jan_avg': avg_january
    }

    return temp_data


# Define the folder containing Excel files
folder_path = "temp_test"

# Initialize a dictionary to store data for each model
models = [
    "WA_Tjul", "WAPLS_Tjul", "MAT_Tjul", "RF_Tjul", "ERT_Tjul", "BRT_Tjul",
    "WA_Tjan", "WAPLS_Tjan", "MAT_Tjan", "RF_Tjan", "ERT_Tjan", "BRT_Tjan"
]
model_data = {model: pd.DataFrame(columns=['Age', 'Temperature']) for model in models}

# Manually assign colors to each model
# Example: We use a list of color names or hex color codes
model_colors = {
    "WA_Tjul": "#332288",
    "WAPLS_Tjul": "#44AA99",
    "MAT_Tjul": "#88CCEE",
    "RF_Tjul": "#882255",
    "ERT_Tjul": "#CC6677",
    "BRT_Tjul": "#DDCC77",
    "WA_Tjan": "#332288",
    "WAPLS_Tjan": "#44AA99",
    "MAT_Tjan": "#88CCEE",
    "RF_Tjan": "#882255",
    "ERT_Tjan": "#CC6677",
    "BRT_Tjan": "#DDCC77"
}

# Process each Excel file
for file in os.listdir(folder_path):
    if file.endswith(".xlsx"):  # Only process Excel files
        file_path = os.path.join(folder_path, file)

        print(f'Handling {file}...')
        
        # Read the Excel file
        df = pd.read_excel(file_path)

        avg_temp_data = get_avg_temp(df, 2000, 3)
        
        if avg_temp_data:
            # Extract the 'Age_cal_a' column and the model columns
            age_column = df["Age_cal_a"]  # Exact column name for 'Age'
            model_columns = df[models]    # Specific columns for the models
            
            # Append data to the corresponding model
            for model in models:
                if 'jul' in model:
                    avg_temp = avg_temp_data['jul_avg']
                if 'jan' in model:
                    avg_temp = avg_temp_data['jan_avg']

                temp_df = pd.DataFrame({
                    'Age': age_column,
                    'Temperature': model_columns[model] - avg_temp
                })

                
                # Check if temp_df contains any non-NaN values before concatenation
                if not temp_df.empty and not temp_df['Temperature'].isna().all():
                    if model_data[model].empty:
                        model_data[model] = temp_df
                    else:
                        # Ensure we only concatenate valid (non-empty, non-NaN) data
                        if not temp_df['Temperature'].isna().all():
                            model_data[model] = pd.concat([model_data[model], temp_df], ignore_index=True)
                
                    model_data[model] = model_data[model].sort_values(by='Age', ascending=True)

# Save plots to a PDF
pdf_path = "model_temperature_plots-FINAL.pdf"
with PdfPages(pdf_path) as pdf:# Iterate through each model and create a separate plot
    for model_name, data in model_data.items():

        print(f'Making pdf {model_name}')

        #print(f'{model_name}: {len(data)}')
        #if model_name == 'BRT_Tjul':
        #    for row in data['Age']:
        #        print(row)
        plt.figure(figsize=(8, 6))  # Create a new figure for each model

        # Filter out non-finite values (necessary for LOESS)
        x = np.array(data['Age'])
        y = np.array(data['Temperature'])
        finite_mask = np.isfinite(x) & np.isfinite(y)  # Mask to keep only finite values
        x = x[finite_mask]
        y = y[finite_mask]

        # Scatter plot of data points
        plt.scatter(x, y, s=10, alpha=0.7, label=model_name, color=model_colors[model_name])

        # Calculate and plot the LOESS smoother for this model (ONE line per model)
        if len(x) > 0 and len(y) > 0:  # Ensure data is available after filtering
            x_out, y_out, _ = loess_1d(x, y, frac=0.1)  # Apply LOESS smoothing (adjust frac for smoothing)
            plt.plot(x_out, y_out, color='black', linestyle='--', label=f'{model_name} LOESS')

        # Add plot details like title and labels
        plt.title(model_name)
        plt.xlabel('Age')
        plt.ylabel('Temperature')
        plt.legend()
        plt.grid(True)
        plt.gca().invert_xaxis()  # Reverse the x-axis direction

        # Save the current figure to the PDF
        pdf.savefig()  # Assuming `pdf` is a PdfPages object
        plt.close()    # Close the figure to free memory


    print(f'Making pdf July all')
    # Plot all July models into one graph with different colors and average lines
    data_for_loess = pd.DataFrame()
    plt.figure(figsize=(10, 8))
    for model_name in [m for m in models if 'jul' in m]:
        data = model_data[model_name]
        data_for_loess = pd.concat([data, data_for_loess], ignore_index=True)
        plt.scatter(data['Age'], data['Temperature'], s=10, alpha=0.7, label=model_name, color=model_colors[model_name])
    
    # Filter out non-finite values (necessary for LOESS)
    data_for_loess = data_for_loess.sort_values(by='Age', ascending=True)
    x = np.array(data_for_loess['Age'])
    y = np.array(data_for_loess['Temperature'])
    finite_mask = np.isfinite(x) & np.isfinite(y)  # Mask to keep only finite values
    x = x[finite_mask]
    y = y[finite_mask]

    # Calculate and plot the LOESS smoother for this model (ONE line per model)
    if len(x) > 0 and len(y) > 0:  # Ensure data is available after filtering
        x_out, y_out, _ = loess_1d(x, y, frac=0.1)  # Apply LOESS smoothing (adjust frac for smoothing)
        plt.plot(x_out, y_out, color='black', linestyle='--', label=f'LOESS')
    
    plt.title('All July Models')
    plt.xlabel('Age')
    plt.ylabel('Temperature')
    plt.legend()
    plt.grid(True)
    plt.gca().invert_xaxis()  # Reverse the x-axis direction
    pdf.savefig()  # Save the current figure to the PDF
    plt.close()

    print(f'Making pdf January all')
    # Plot all January models into one graph with different colors and average lines
    data_for_loess = pd.DataFrame()
    plt.figure(figsize=(10, 8))
    for model_name in [m for m in models if 'jan' in m]:
        data = model_data[model_name]
        data_for_loess = pd.concat([data, data_for_loess], ignore_index=True)
        plt.scatter(data['Age'], data['Temperature'], s=10, alpha=0.7, label=model_name, color=model_colors[model_name])
    
    # Filter out non-finite values (necessary for LOESS)
    data_for_loess = data_for_loess.sort_values(by='Age', ascending=True)
    x = np.array(data_for_loess['Age'])
    y = np.array(data_for_loess['Temperature'])
    finite_mask = np.isfinite(x) & np.isfinite(y)  # Mask to keep only finite values
    x = x[finite_mask]
    y = y[finite_mask]

    # Calculate and plot the LOESS smoother for this model (ONE line per model)
    if len(x) > 0 and len(y) > 0:  # Ensure data is available after filtering
        x_out, y_out, _ = loess_1d(x, y, frac=0.1)  # Apply LOESS smoothing (adjust frac for smoothing)
        plt.plot(x_out, y_out, color='black', linestyle='--', label=f'LOESS')
    
    
    plt.title('All January Models')
    plt.xlabel('Age')
    plt.ylabel('Temperature')
    plt.legend()
    plt.grid(True)
    plt.gca().invert_xaxis()  # Reverse the x-axis direction
    pdf.savefig()  # Save the current figure to the PDF
    plt.close()

print(f"Plots have been saved to {pdf_path}")
