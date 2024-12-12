import numpy as np
import pandas as pd
import os
from io import StringIO
import matplotlib.pyplot as plt
from scipy.interpolate import griddata, Rbf

# Base folder path to search for .ags files
base_folder_path = r'C:\Users\10024680\Downloads\02-PHASE 2 (1)\02-PHASE 2\05- AGS FILE\Phase 2B-B'

# Output directory for contour maps
save_directory = r"C:\Users\10024680\Downloads"

# Property to filter for contour mapping
property_filter = 'F1(m)'  # Replace with the desired property column name

def process_ags_file(file_path):
    """
    Parse .ags file and extract relevant columns for `HOLE` and `GEOL`.
    """
    in_GEOL = False
    in_HOLE = False

    geol_lines = []
    hole_lines = []

    # Extract HOLE data
    with open(file_path, 'r') as file:
        for line in file:
            if "**HOLE" in line:
                in_HOLE = True
                continue
            if in_HOLE:
                if len(line) == 9:
                    break
                hole_lines.append(line.strip())
    data_hole = StringIO('\n'.join(hole_lines))

    df_hole = pd.read_csv(data_hole)
    columns_to_keep = ['*HOLE_ID', '*HOLE_NATE', '*HOLE_NATN', '*HOLE_GL']
    df_hole = df_hole[columns_to_keep].dropna()
    df_hole.columns = ['BH NO', 'EASTING', 'NORTHING', 'RL(m)']
    df_hole = df_hole.drop(index=0).reset_index(drop=True)

    # Extract GEOL data
    with open(file_path, 'r') as file:
        for line in file:
            if "**GEOL" in line:
                in_GEOL = True
                continue
            if in_GEOL:
                if len(line) == 9:
                    break
                geol_lines.append(line.strip())

    data_geol = StringIO('\n'.join(geol_lines))
    df_geol = pd.read_csv(data_geol)
    columns_to_keep = ['*GEOL_TOP', '*GEOL_BASE', '*GEOL_GEOL']
    df_geol = df_geol[columns_to_keep].dropna()
    df_geol.columns = ['GEOL_TOP', 'GEOL_BASE', 'GEOL_GEO3']
    df_geol['Layer_Thickness'] = pd.to_numeric(df_geol['GEOL_BASE'], errors='coerce') - pd.to_numeric(df_geol['GEOL_TOP'], errors='coerce')

    # Combine `HOLE` and `GEOL` data
    combined_dict = df_hole.iloc[0].to_dict()
    layer_summary = df_geol.groupby('GEOL_GEO3')['Layer_Thickness'].sum().reset_index()
    geol_dict = dict(zip(layer_summary['GEOL_GEO3'], layer_summary['Layer_Thickness']))

    combined_dict.update(geol_dict)
    return pd.DataFrame([combined_dict])

def generate_contour_map(data, property_name, save_path):
    """
    Generate and save a contour map from the data.
    """
    easting = data['EASTING']
    northing = data['NORTHING']
    property_values = data[property_name].fillna(0)

    # Define grid for interpolation
    grid_x, grid_y = np.meshgrid(
        np.linspace(easting.min(), easting.max(), 200),
        np.linspace(northing.min(), northing.max(), 200)
    )

    # Interpolation using RBF
    rbf = Rbf(easting, northing, property_values, function='linear')
    grid_z = rbf(grid_x, grid_y)

    # Clip extreme values for better visualization
    levels = np.linspace(property_values.quantile(0.01), property_values.quantile(0.99), 20)

    # Plot contour map
    plt.figure(figsize=(12, 10))
    contour_filled = plt.contourf(grid_x, grid_y, grid_z, levels=levels, cmap='Spectral', extend='both')
    contour_lines = plt.contour(grid_x, grid_y, grid_z, levels=levels, colors='black', linewidths=0.5)
    plt.clabel(contour_lines, inline=True, fontsize=8, fmt="%.1f")
    plt.scatter(easting, northing, c='black', s=10, label='Data Points')

    # Add colorbar
    cbar = plt.colorbar(contour_filled)
    cbar.set_label(f"{property_name} (m)")

    # Finalize plot
    plt.title(f"{property_name} Contour Map", fontsize=14)
    plt.xlabel("EASTING (m)", fontsize=12)
    plt.ylabel("NORTHING (m)", fontsize=12)
    plt.legend(loc='upper right')
    plt.gca().set_aspect('equal', adjustable='box')

    # Save plot
    plt.savefig(save_path, dpi=300)
    plt.show()
    print(f"Contour map saved to: {save_path}")

# Main workflow
if __name__ == "__main__":
    all_data = []

    for root, dirs, files in os.walk(base_folder_path):
        for file in files:
            if file.lower().endswith(".ags"):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                df = process_ags_file(file_path)
                all_data.append(df)

    # Combine all data
    combined_data = pd.concat(all_data, ignore_index=True)

    # Generate contour map
    contour_save_path = os.path.join(save_directory, f"{property_filter}_contour_map_combined.png")
    generate_contour_map(combined_data, property_filter, contour_save_path)
