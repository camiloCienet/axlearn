#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Check if the correct number of arguments are provided.
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <GCS_URL> <RUN_ID>"
  exit 1
fi

# gs://axlearn-arc-testing/testing/results/archive/cpu-unit-tests-5d250e5-0.7.2.dev20250914-17836834329-2025-09-18-17:52:21.tar.gz
#
CURRENT_FOLDER=$(pwd)
echo "The current folder is: $CURRENT_FOLDER"

GCS_URL="$1"
DESTINATION_PATH="${CURRENT_FOLDER}/raw_csv_file.tar.gz"
RUN_ID="$2" # RUN_ID should be the third argument

# Create the new directory for extraction
EXTRACT_DIR="${CURRENT_FOLDER}/run_#${RUN_ID}"
mkdir -p "$EXTRACT_DIR"

echo "Downloading $GCS_URL to $DESTINATION_PATH..."
gsutil cp "$GCS_URL" "$DESTINATION_PATH"
echo "Download complete."

# Un-tar the downloaded file into the newly created directory.
echo "Extracting contents to $EXTRACT_DIR..."
tar -xzf "$DESTINATION_PATH" -C "$EXTRACT_DIR"
echo "Extraction complete."

# Now from csv folder get all unique tests using reader.py
python reader.py $EXTRACT_DIR

