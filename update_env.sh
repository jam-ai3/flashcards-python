#!bin/bash

set -e

ENV_NAME="extractor"

ENV_FILE="./env.yml"

source "/home/ec2-user/miniconda3/etc/profile.d/conda.sh"

if [ ! -f "$ENV_FILE" ]; then
  echo "Error: $ENV_FILE not found."
  exit 1
fi

echo "Updating the $ENV_NAME environment with $ENV_FILE..."
conda env update --name "$ENV_NAME" --file "$ENV_FILE" --prune

echo "Environment '$ENV_NAME' updated successfully."