npm install exceljs d3
const ExcelJS = require('exceljs');
const d3 = require('d3');

async function createContourMap() {
  try {
    // Read Excel file
    const workbook = new ExcelJS.Workbook();
    await workbook.xlsx.readFile('/Volumes/STEPH 64GB/SJ/Soil Contour/02-PHASE 2 (1)/02-PHASE 2/05- AGS FILE/Phase-2.xlsx');
    const worksheet = workbook.worksheets[0]; // Assuming data is in the first sheet

    // Extract data from Excel
    const data = [];
    worksheet.eachRow({ includeEmpty: true }, (row, rowNumber) => {
      if (rowNumber > 1) { // Assuming header row
        data.push({
          x: row.getCell(1).value,
          y: row.getCell(2).value,
          z: row.getCell(3).value
        });
      }
    });

    // Create SVG container
    const svg = d3.select("body")
      .append("svg")
      .attr("width", 800)
      .attr("height", 600);

    // Create scales for x, y, and z axes
    const xScale = d3.scaleLinear()
      .domain([d3.min(data, d => d.x), d3.max(data, d => d.x)])
      .range([50, 750]);

    const yScale = d3.scaleLinear()
      .domain([d3.min(data, d => d.y), d3.max(data, d => d.y)])
      .range([50, 550]);

    const colorScale = d3.scaleSequential()
      .domain([d3.min(data, d => d.z), d3.max(data, d => d.z)])
      .interpolator(d3.interpolateViridis);

    // Create contour generator
    const contourGenerator = d3.contourDensity()
      .x(d => xScale(d.x))
      .y(d => yScale(d.y))
      .size([700, 500])
      .bandwidth(20)
      .thresholds(20);

    // Generate contours
    const contours = contourGenerator(data);

    // Render contours on SVG
    svg.selectAll("path")
      .data(contours)
      .enter()
      .append("path")
      .attr("d", d3.geoPath())
      .attr("fill", d => colorScale(d.value))
      .attr("stroke", "black")
      .attr("stroke-width", 0.5);
  } catch (error) {
    console.error("Error:", error);
  }
}

createContourMap();