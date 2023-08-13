#!/bin/zsh

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Source the files if they exist
[[ -f ~/.zprofile ]] && source ~/.zshenv
[[ -f ~/.zshrc ]] && source ~/.zshrc

# Call your Python script, using a relative path
"$SCRIPT_DIR/dist/main" "$@"
