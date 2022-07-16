#!/bin/bash

search_dir="$1"
output_dir="$2"
for entry in "$search_dir"/*
do
  echo $entry
  python3 ./image_optimizer/main.py $entry "$output_dir/$(basename $entry)"
done