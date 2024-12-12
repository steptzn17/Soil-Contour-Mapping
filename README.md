# Soil Contour Mapping

Started during my internship. I decided to continue diving into this area as I gained interest in it. Tried to code in other languages besides Python

## Soil Contouring Using Python

This project automates the generation of soil contour maps, leveraging Python's data analysis and visualization libraries to process geospatial and soil data efficiently. Soil contour maps represent variations in soil properties over a geographical area, making them vital tools in civil engineering, agriculture, and environmental studies.

## Features

- **Data Handling**: Efficiently reads and processes soil data from AGS files.  
- **Interpolation**: Implements advanced interpolation methods using `scipy` to create smooth contour lines.  
- **Visualization**: Generates professional-quality contour maps using `matplotlib`.  
- **Customization**: Allows flexible adjustments for data inputs, color schemes, and contour intervals.

### Technologies Used

- **Python Libraries**:  
  - `numpy`: For numerical computations.  
  - `pandas`: For data manipulation.  
  - `scipy`: For spatial interpolation.  
  - `matplotlib`: For contour plotting.

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/soil-contouring.gitcd soil-contouring
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the script:
   python soil_mapping.py

## Use Cases

- **Civil Engineering**: Designing drainage, foundations, and land grading based on soil properties.
- **Agriculture**: Understanding soil fertility patterns for optimized crop management.
- **Environmental Studies**: Identifying areas prone to erosion or contamination.

## Project Structure

- data/                   # Input soil data files (e.g., AGS format)
- outputs/                # Generated contour maps
- soil_mapping.py         # Main Python script
- requirements.txt        # Dependencies
- README.md               # Project description

## Future Improvements

- Integration with GIS tools for geospatial analysis.
- Support for additional file formats and real-time data.
- Enhanced 3D visualization of soil profiles.

## Applications used:
- Spyder
- Visual Studio Code
- Google Colab

## Disclaimer:
This is my first time trying other programming languages other than Python. There are errors so please do take note haha

