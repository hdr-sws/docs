const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

// Configuration
const sourceDir = process.argv[2] || './svg'; // Default to './svg' if no argument provided
const outputDir = process.argv[3] || './png'; // Default to './png' if no argument provided
const width = process.argv[4] ? parseInt(process.argv[4]) : 1024; // Default width: 1024px

// Ensure output directory exists
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// Check if source directory exists
if (!fs.existsSync(sourceDir)) {
  console.error(`Error: Source directory '${sourceDir}' does not exist.`);
  process.exit(1);
}

// Get all SVG files from the source directory
const svgFiles = fs.readdirSync(sourceDir)
  .filter(file => file.toLowerCase().endsWith('.svg'));

if (svgFiles.length === 0) {
  console.log(`No SVG files found in '${sourceDir}'.`);
  process.exit(0);
}

console.log(`Found ${svgFiles.length} SVG files. Converting...`);

// Process each SVG file
let completed = 0;
let errors = 0;

svgFiles.forEach(file => {
  const inputPath = path.join(sourceDir, file);
  const outputPath = path.join(outputDir, file.replace(/\.svg$/i, '.png'));
  
  sharp(inputPath)
    .resize({ width })
    .png()
    .toFile(outputPath)
    .then(() => {
      completed++;
      console.log(`Converted: ${file} -> ${path.basename(outputPath)}`);
      
      if (completed + errors === svgFiles.length) {
        console.log(`\nConversion complete! ${completed} files converted, ${errors} errors.`);
      }
    })
    .catch(err => {
      errors++;
      console.error(`Error converting ${file}: ${err.message}`);
      
      if (completed + errors === svgFiles.length) {
        console.log(`\nConversion complete! ${completed} files converted, ${errors} errors.`);
      }
    });
});

console.log('Processing files...'); 