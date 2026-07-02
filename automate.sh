#!/bin/bash

# Usage: ./run_grype.sh [directory]
# Default to current directory if none provided
TARGET_DIR="${1:-.}"

# Check if directory exists
if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Error: Directory '$TARGET_DIR' not found."
  exit 1
fi

# Find all .tar files in the target directory
TAR_FILES=("$TARGET_DIR"/*.tar)

# Check if any .tar files exist
if [[ ! -e "${TAR_FILES[0]}" ]]; then
  echo "No .tar files found in '$TARGET_DIR'."
  exit 0
fi

echo "Found ${#TAR_FILES[@]} .tar file(s) in '$TARGET_DIR'."
echo "----------------------------------------"

mkdir "$TARGET_DIR/result"

for TAR_FILE in "${TAR_FILES[@]}"; do
  # Get the base filename without extension (e.g. "myimage" from "myimage.tar")
  BASE_NAME=$(basename "$TAR_FILE" .tar)
  OUTPUT_FILE="$TARGET_DIR/result/${BASE_NAME}.json"

  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Scanning: $TAR_FILE"
  echo "  Output -> $OUTPUT_FILE"

  grype "$TAR_FILE" -o json > "$OUTPUT_FILE"

  if [[ $? -eq 0 ]]; then
    echo "  Status : Done"
  else
    echo "  Status : grype exited with an error (check $OUTPUT_FILE)"
  fi

  echo "  Waiting 3 seconds..."
  sleep 3
done

echo "----------------------------------------"
echo "All scans complete."
