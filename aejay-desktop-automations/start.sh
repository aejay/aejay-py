#!/bin/sh
# Source the appropriate profile file
if [ -n "$ZSH_VERSION" ]; then
    source ~/.zshrc
elif [ -n "$BASH_VERSION" ]; then
    source ~/.bashrc
else
    echo "Script only supports bash and zsh"
    exit 1
fi

# Now we can use the asdf shims
python /Users/aejay/Repos/aejay-py/aejay-automations/main.py
