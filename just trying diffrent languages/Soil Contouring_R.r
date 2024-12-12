# Install required packages (if not already installed)
if (!require("readxl")) install.packages("readxl")
if (!require("gridExtra")) install.packages("gridExtra")
if (!require("dendext")) install.packages("dendext")  # For interpolation (alternative to interp)
# Load libraries
library(readxl)
library(gridExtra)
library(dendext)  # For interpolation

# Define file path (replace with your actual path)
file_path <- "/Volumes/STEPH 64GB/SJ/Soil Contour/Phase-2A-A.xlsx"

# Read Excel data
try {
  df <- read_excel(file_path)
  print("Data loaded successfully!")
  print(head(df))  # Show first few rows
} catch(error) {
  print(paste("Error loading Excel file:", error))
  quit(status = 1)
}

# Validate required columns
required_cols <- c("EASTING", "NORTHING", "Fill(m)", "F1(m)", "Clay(m)")
if (!all(required_cols %in% names(df))) {
  print(paste("Error: Excel file must contain columns:", required_cols, collapse = ", "))
  quit(status = 1)
}

# Choose property for filtering (replace with your preference)
property <- "Clay(m)"

# Extract relevant columns
easting <- df$EASTING
northing <- df$NORTHING
thickness <- df[, property]

# Create grid for interpolation
grid_x <- seq(min(easting), max(easting), length.out = 100)
grid_y <- seq(min(northing), max(northing), length.out = 100)
grid <- expand.grid(grid_x, grid_y)

# Interpolate data (using interp from dendext package)
try {
  grid_z <- interp(easting, northing, thickness, grid = grid, method = "cubic")
  print("Interpolation successful!")
} catch(error) {
  print(paste("Error during interpolation:", error))
  quit(status = 1)
}

# Generate contour plot
library(ggplot2)  # Assuming ggplot2 is installed
ggplot(aes(x = grid_x, y = grid_y, z = grid_z)) +
  geom_raster(fill = grid_z, aes(fill = grid_z)) +
  scale_fill_gradient(name = paste(property, " Thickness (m)"), low = min(grid_z), high = max(grid_z)) +
  labs(title = paste(property, "Contour Map"), x = "EASTING (m)", y = "NORTHING (m)") +
  theme_bw()  # Adjust theme as desired

# Save plot (replace with your desired format and path)
ggsave(paste0(property, "_contour_map.png"), width = 10, height = 8)

print(paste("Contour map saved!"))
