#!/usr/bin/env bash

set -e

# Function to print error messages
error() {
    echo "Error: $1" >&2
    exit 1
}

# Check if 'uv' is installed
if ! command -v uv &> /dev/null; then
    error "uv is not installed. Please install it from https://astral.sh/uv/"
    exit 1
fi

echo "uv is installed."
exit 0 