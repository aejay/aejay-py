#!/bin/zsh

if [[ -f ~/.zshrc ]]; then
  source ~/.zshrc
fi

DIR="${0:a:h}"

python "$DIR/main.py"
