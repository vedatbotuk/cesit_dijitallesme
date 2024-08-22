#!/bin/bash

# Define source and destination files
SOURCE_FILE="conf/setup_example.json"
DESTINATION_FILE="setup.json"

# Check if the source file exists
if [ ! -f "$SOURCE_FILE" ]; then
  echo "Error: The source file '$SOURCE_FILE' does not exist."
  exit 1
fi

# Copy the file and rename it
cp "$SOURCE_FILE" "$DESTINATION_FILE"

# Check if the copy operation was successful
if [ $? -eq 0 ]; then
  echo "File successfully copied and renamed to '$DESTINATION_FILE'."
else
  echo "Error: The file could not be copied."
  exit 1
fi

# Install Python packages from requirements.txt
echo "Installing required Python packages from requirements.txt..."

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
  echo "Error: requirements.txt file not found."
  exit 1
fi

pip3 install -r conf/requirements.txt

# Check if the pip install was successful
if [ $? -eq 0 ]; then
  echo "Python packages successfully installed."
else
  echo "Error: Python packages could not be installed."
  exit 1
fi
