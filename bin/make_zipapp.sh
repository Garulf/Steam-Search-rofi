#!/bin/sh

NAME="Steam-Search-Rofi"

mkdir -p dist
python3 -m zipapp src -o "dist/$NAME.pyz"
