#!/bin/bash

# Production build script for GitHub Pages deployment
# This script builds the site with the correct basepath for GitHub Pages

echo "Building site for production deployment..."

# Build the site with the GitHub Pages basepath
python3 src/main.py "/StaticSiteGenerator/"

echo "Production build completed! Site is ready for GitHub Pages deployment."
