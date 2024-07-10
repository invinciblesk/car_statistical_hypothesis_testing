import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure the img directory exists
img_directory = 'img/'
if not os.path.exists(img_directory):
    os.makedirs(img_directory)

# Load the CSV file into a DataFrame
df_cars = pd.read_csv('data/cars.csv')

# Define a color map for the origins
color_map = {'USA': 'blue', 'Germany': 'red', 'Japan': 'green'}

# Check if 'origin_name' column exists, if not, create it
if 'origin_name' not in df_cars.columns:
    origin_names = {1: 'USA', 2: 'Germany', 3: 'Japan'}
    # Assuming 'origin' is the column with country codes
    df_cars['origin_name'] = df_cars['origin'].map(origin_names)

# Convert 'horsepower' to numeric, coercing errors to NaN, then drop these missing values
df_cars['horsepower'] = pd.to_numeric(df_cars['horsepower'], errors='coerce')
df_cars.dropna(subset=['horsepower'], inplace=True)

# Plotting scatter plots for numerical columns
numerical_cols = df_cars.select_dtypes(include=['int64', 'float64']).columns.tolist()
num_plots = len(numerical_cols) * (len(numerical_cols) - 1) // 2
grid_size = int(np.ceil(np.sqrt(num_plots)))
fig, axes = plt.subplots(grid_size, grid_size, figsize=(grid_size * 5, grid_size * 4))
fig.subplots_adjust(hspace=0.4, wspace=0.4)
axes_flat = axes.flatten()
plot_idx = 0

for i, col1 in enumerate(numerical_cols):
    for col2 in numerical_cols[i+1:]:
        ax = axes_flat[plot_idx]
        sns.scatterplot(data=df_cars, x=col1, y=col2, hue='origin_name', palette=color_map, ax=ax)
        ax.set_title(f'{col1} vs {col2}')
        ax.set_xlabel(col1)
        ax.set_ylabel(col2)
        ax.legend(title='Origin', loc='upper right')
        plot_idx += 1

for idx in range(plot_idx, len(axes_flat)):
    axes_flat[idx].set_visible(False)

plt.savefig(os.path.join(img_directory, 'origin.png'))

# Plotting histograms for 'mpg', 'weight', 'horsepower', and origin counts
fig, axs = plt.subplots(2, 2, figsize=(10, 10))
df_cars['mpg'].plot(kind='hist', ax=axs[0, 0], title='MPG Distribution')
df_cars['weight'].plot(kind='hist', ax=axs[0, 1], title='Weight Distribution')
df_cars['horsepower'].plot(kind='hist', ax=axs[1, 0], title='Horsepower Distribution')
df_cars['origin_name'].value_counts().plot(kind='bar', ax=axs[1, 1], title='Origin Counts')
plt.tight_layout()
plt.savefig(os.path.join(img_directory, 'part-1_origin_counts.png'))

# Plotting MPG distributions for Japan vs. USA
plt.figure(figsize=(10, 6))
japan_mpg = df_cars[df_cars['origin_name'] == 'Japan']['mpg']
usa_mpg = df_cars[df_cars['origin_name'] == 'USA']['mpg']
plt.hist(japan_mpg, alpha=0.5, label='Japan', bins=20)
plt.hist(usa_mpg, alpha=0.5, label='USA', bins=20)
plt.title('MPG Distributions: Japan vs. USA')
plt.xlabel('Miles Per Gallon (MPG)')
plt.ylabel('Frequency')
plt.legend()
plt.savefig(os.path.join(img_directory, 'part-2_japan_vs_usa.png'))

# Plotting distributions and performing Mann-Whitney U tests for 'mpg', 'weight', 'horsepower'
fig, axs = plt.subplots(3, 1, figsize=(15, 30))
for ax, feature in zip(axs, ['mpg', 'weight', 'horsepower']):
    sns.histplot(df_cars[df_cars['origin_name'] == 'USA'][feature], bins=40, kde=True, color='blue', ax=ax, label='USA')
    sns.histplot(df_cars[df_cars['origin_name'] == 'Germany'][feature], bins=40, kde=True, color='red', ax=ax, label='Germany')
    sns.histplot(df_cars[df_cars['origin_name'] == 'Japan'][feature], bins=40, kde=True, color='green', ax=ax, label='Japan')
    ax.set_title(f'{feature.capitalize()} Distributions')
    ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(img_directory, 'part-3_distributions_and_tests.png'))