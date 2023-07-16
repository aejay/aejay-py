#!/bin/zsh

if [[ -f ~/.zshrc ]]; then
  source ~/.zshrc
fi

DIR="${0:a:h}"

source "$DIR/venv/bin/activate"

python "$DIR/main.py"
