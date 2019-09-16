#!/bin/bash

# Schell Script to Download Files from S3 Bucket

echo "Checking directory existance for models..."

if [ -d "/usr/src/app/models" ]
then
    echo "Models directory exist!"
else
    mkdir -p /usr/src/app/models
fi

echo "Downloading models..."

python3 /usr/src/app/scripts/download_files.py
