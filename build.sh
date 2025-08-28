#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create any necessary directories
mkdir -p data

echo "Build completed successfully!"