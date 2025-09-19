#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Go one folder previous

# Define the name and tag for the Docker image
IMAGE_NAME="axlearn-test-environment"
TAG="latest"
PROJECT_ROOT=$(pwd)

# 1. Build the Docker Image
# This command targets the 'ci' stage in your multi-stage Dockerfile.
# The 'ci' stage includes the execution of your unit tests.
echo "--- 1. Building Docker image: ${IMAGE_NAME}:${TAG} (Target: ci) ---"
docker build \
  --target ci \
  --tag ${IMAGE_NAME}:${TAG} \
  .

# Check if the build was successful
if [ $? -ne 0 ]; then
  echo "Docker build failed. Exiting."
  exit 1
fi

# docker run -v $(pwd)/axlearn:/root/axlearn -it --name my-container axlearn-ci-test /bin/bash
# 2. Run a container from the built image
# This runs the container interactively (-it) and removes it after exit (--rm).
echo "--- 2. Running container from ${IMAGE_NAME}:${TAG} ---"
docker run \
  -d \
  --name axlearn_test_container \
  -v ${PROJECT_ROOT}/axlearn:/root/axlearn\
  ${IMAGE_NAME}:${TAG} \
  tail -f /dev/null

echo "--- Container exited. ---"

# Building the image


# docker run -v $(pwd)/axlearn:/root/axlearn -it --name my-container axlearn-ci-test /bin/bash

