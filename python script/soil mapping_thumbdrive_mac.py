#This was done on a Macbook and data was extracted from a thumbdrive. Hence, the name of this file.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import os

# Define the path to your Excel file
file_path = '/Volumes/STEPH 64GB/SJ/Soil Contour/Phase-2A-A.xlsx'

# Load the Excel file
try:
    df = pd.read_excel(file_path)
    print("Data loaded successfully!")
    print(df.head())  
except FileNotFoundError:
    print("Error: File not found. Check the file path.")
    exit()
except Exception as e:
    print(f"Error loading Excel file: {e}")
    exit()

# Validate required columns
required_columns = ['EASTING', 'NORTHING', 'Fill(m)', 'F1(m)', 'Clay(m)']
if not all(col in df.columns for col in required_columns):
    print(f"Error: Excel file must contain columns: {required_columns}")
    exit()

# Filter for a specific property (e.g., "Fill(m)")
property_filter = 'Clay(m)'  # Change this to 'F1(m)' or 'Clay(m)' as needed
if property_filter not in df.columns:
    print(f"Error: Column '{property_filter}' not found in data.")
    exit()

# Extract relevant columns
easting = df['EASTING']
northing = df['NORTHING']
thickness = df[property_filter]

# Create a grid for interpolation
grid_x, grid_y = np.meshgrid(
    np.linspace(easting.min(), easting.max(), 100),
    np.linspace(northing.min(), northing.max(), 100)
)

# Interpolate the data
try:
    grid_z = griddata(
        points=(easting, northing),
        values=thickness,
        xi=(grid_x, grid_y),
        method='cubic'
    )
    print("Interpolation successful!")
except Exception as e:
    print(f"Error during interpolation: {e}")
    exit()

# Plot the contour map
plt.figure(figsize=(10, 8))
contour = plt.contourf(grid_x, grid_y, grid_z, levels=15, cmap='Spectral')
plt.colorbar(contour, label=f"{property_filter} Thickness (m)")
plt.title(f"{property_filter} Contour Map")
plt.xlabel("EASTING (m)")
plt.ylabel("NORTHING (m)")

# Save the contour plot
save_directory = r"/Volumes/STEPH 64GB/SJ/Soil Contour/02-PHASE 2 (1)/02-PHASE 2/05- AGS FILE"  # Update to your desired directory
if not os.path.exists(save_directory):
    os.makedirs(save_directory)  # Create directory if it doesn't exist

save_path = f"{save_directory}\\{property_filter.replace('/', '_')}_contour_map.png"
plt.savefig(save_path)
plt.show()

print(f"Contour map saved at '{save_path}'.")
