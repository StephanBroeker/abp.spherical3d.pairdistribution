#!/bin/bash

# -- Shell script for collecting files for distribution --

# Check for self to see if directory is correct
if [ ! -f "./makeDist.sh" ]; then
  echo "Error: Please cd to /supp."
  exit
fi
# Clean old dist
if [ -d "dist" ]; then
  echo "Removing old /dist..."
  rm -r "dist"
fi
# Make doc
echo "Creating documentation..."
. makeDoc.sh
# Collect files
echo "Collecting files..."
mkdir "dist"
cp -R "abp3d" "dist"
if [ -d "dist/abp3d/__pycache__" ]; then
  rm -r "dist/abp3d/__pycache__"
fi
cp "demo.py" "dist/"
cp -R "doc/abp3d" "dist/doc"
cp "abp3d/fitparams.csv" "dist/"
cp "README.md" "dist/"

echo "Done!"
