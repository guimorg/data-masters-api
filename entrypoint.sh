#!/bin/bash

# Entrypoint for applicatio
# first we need to download all files from models

echo "Checking directory existance for models..."

if [ -d "/usr/src/app/models" ]
then
    echo "Models directory exist!"
else
    mkdir -p /usr/src/app/models
fi

echo "Downloading models..."

python3 /usr/src/app/scripts/download_files.py

# and then we execute what we need

echo "Starting application..."

python3 -m api
