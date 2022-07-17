#!/bin/bash

source_dir="$1"
output_dir="$2"

python3 ./formula_describer/main.py $source_dir "$source_dir/dataset.json"
mkdir -p "$output_dir"
rm -r  "$output_dir"
cp -r "$source_dir" "$output_dir"
