#!/bin/bash

# Generate the static site
python3 src/main.py

# Start the web server in the docs directory
cd docs && python3 -m http.server 8888
