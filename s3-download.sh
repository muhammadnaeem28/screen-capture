#!/bin/bash

set -e

# Configure environment variables
SCRIPTS_DIR="$CICD_SCRIPTS_DIR/$(dirname "${BASH_SOURCE[0]}")"
export CONFIG_DIR="${CONFIG_DIR:-config}"

# Use deployment role to download s3 bucket objects.
source "$CONFIG_DIR/environment/aws.env" && echo "Loaded aws.env"
source "$SCRIPTS_DIR/assume-role.sh" "$AWS_REGION" "$CI_RUNNER_ID" "$DEPLOYMENT_ROLE"

grep "S3_OBJECT_URI=s3://" "$1" | while read -r line; do
    S3_FILE="$(echo "$line" | grep -Eo 's3://[^ ]+')"
    aws s3 cp "$S3_FILE" . 
done

