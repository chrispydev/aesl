#!/bin/bash

MAIN_DIR="$(pwd)"

echo "Collecting images from subfolders..."

find "$MAIN_DIR" -mindepth 2 -type f \( \
  -iname "*.jpg" \
  -o -iname "*.jpeg" \
  -o -iname "*.png" \
  -o -iname "*.JPG" \
  \) -print0 | while IFS= read -r -d '' file; do
  filename=$(basename "$file")
  destination="$MAIN_DIR/$filename"

  # Prevent duplicate overwrite
  if [ -e "$destination" ]; then
    name="${filename%.*}"
    ext="${filename##*.}"
    count=1

    while [ -e "$MAIN_DIR/${name}_${count}.${ext}" ]; do
      count=$((count + 1))
    done

    destination="$MAIN_DIR/${name}_${count}.${ext}"
  fi

  echo "Moving: $file"
  mv "$file" "$destination"
done

echo "Removing empty folders..."

find "$MAIN_DIR" -type d -empty ! -path "$MAIN_DIR" -delete

echo "Completed."
