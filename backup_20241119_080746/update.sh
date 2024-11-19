#!/bin/bash

# Create backup
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR
cp -r * $BACKUP_DIR/

# Update files from module_files.txt
csplit --quiet --prefix=part module_files.txt "/^=== /" {*}

for file in part*; do
    FILEPATH=$(head -n 1 "$file" | grep -o '[^=].*[^=]' | xargs)
    if [ "$FILEPATH" != "Module Files" ]; then
        mkdir -p $(dirname "$FILEPATH")
        tail -n +2 "$file" > "$FILEPATH"
    fi
    rm "$file"
done

echo "Files updated successfully"