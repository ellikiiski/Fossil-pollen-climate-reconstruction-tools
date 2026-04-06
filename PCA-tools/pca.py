import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Input file
excel_file = 'combined_pollen_data_all_sites.xlsx'

# Load data
df = pd.read_excel(excel_file)

# Remove age column (assumed to be first column)
df = df.iloc[:, 1:]

# Transpose so that samples are rows
x = df.T.values
labels = df.columns.tolist()

# CLR TRANSFORMATION
pseudocount = 1e-6
x = x + pseudocount

# Compute geometric mean for each sample (row-wise)
geo_mean = np.exp(np.mean(np.log(x), axis=1)).reshape(-1, 1)

# Apply CLR transformation
x_clr = np.log(x / geo_mean)

# PCA (2 components for plotting)
pca = PCA(n_components=2)
pca_clr = pca.fit_transform(x_clr)
var_clr = pca.explained_variance_ratio_

# PCA (5 components for explained variance)
pca_full = PCA(n_components=5)
pca_full.fit(x_clr)
var_full = pca_full.explained_variance_ratio_

print("\nExplained variance (first 5 principal components):")
for i, var in enumerate(var_full, start=1):
    print(f"PC{i}: {var*100:.2f}%")

# PLOTTING
color_map = plt.cm.get_cmap("viridis", len(labels))
label_color_map = {label: color_map(i) for i, label in enumerate(labels)}

plt.figure(figsize=(8, 6))

for i, label in enumerate(labels):
    plt.scatter(
        pca_clr[i, 0],
        pca_clr[i, 1],
        alpha=0.7,
        edgecolors='k',
        color=label_color_map[label],
        s=50
    )
    plt.text(
        pca_clr[i, 0],
        pca_clr[i, 1],
        f'   {label}',
        fontsize=6,
        ha='left',
        va='center'
    )

plt.title('PCA of CLR-transformed pollen data')
plt.xlabel(f'PC1 ({var_clr[0]*100:.1f}%)')
plt.ylabel(f'PC2 ({var_clr[1]*100:.1f}%)')
plt.grid(False)

plt.tight_layout()
plt.savefig('pca_clr_plot.png', dpi=300, bbox_inches='tight')