#!/usr/bin/env bash

set -e

# Check if Python 3.13 is already the global default
CURRENT_PYTHON_VERSION=$(python --version 2>&1)
if [[ $CURRENT_PYTHON_VERSION == Python\ 3.13* ]]; then
    echo "Python 3.13 is already the global default."
    exit 0
else
    echo "Python 3.13 is not the global default. Current version: $CURRENT_PYTHON_VERSION"
    exit 1
fi 