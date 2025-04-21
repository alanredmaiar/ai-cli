#!/usr/bin/env bash

set -e

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CHECKERS_DIR="$SCRIPT_DIR/../checkers"

# Function to print error messages
error() {
    echo "Error: $1" >&2
    exit 1
}

# Check if uv is installed
if ! bash "$CHECKERS_DIR/check_uv.sh"; then
    error "uv check failed. Exiting."
fi

# Check if Python 3.13 is already installed
if bash "$CHECKERS_DIR/check_python.sh"; then
    echo "Python 3.13 is already installed. Nothing to do."
    exit 0
fi

# Install Python 3.13 using uv
echo "Installing Python 3.13 using uv..."
uv python install 3.13

# Get the shell configuration file
SHELL_RC=$(bash "$CHECKERS_DIR/check_bash.sh")
echo "Detected shell configuration: $SHELL_RC"

# Define the function to set 'python' to Python 3.13
PYTHON_FUNC='
# Set python to Python 3.13
python() {
    "$(uv python find 3.13)" "$@"
}
'

# Check if the function is already in the shell configuration
if ! grep -Fxq "# Set python to Python 3.13" "$SHELL_RC"; then
    echo "Adding python function to $SHELL_RC..."
    echo "$PYTHON_FUNC" >> "$SHELL_RC"
else
    echo "Python function already exists in $SHELL_RC."
fi

# Source the shell configuration to apply changes
echo "Sourcing $SHELL_RC..."
# shellcheck source=/dev/null
source "$SHELL_RC"

# Verify that 'python' points to Python 3.13
PYTHON_VERSION=$(python --version 2>&1)
if [[ $PYTHON_VERSION == Python\ 3.13* ]]; then
    echo "Success: 'python' points to $PYTHON_VERSION"
else
    echo "Warning: 'python' points to $PYTHON_VERSION"
    echo "Please ensure that 'uv' has installed Python 3.13 correctly."
fi

echo "Python 3.13 installation completed."
exit 0