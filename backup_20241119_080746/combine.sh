#!/bin/bash

# Auto-detect all files recursively
find . -type f \( -name "*.py" -o -name "*.xml" -o -name "*.csv" \) -not -path "./backup*" -not -name "*.sh" | while read file; do
    echo -e "\n=== $file ===" >> module_files.txt
    cat "$file" >> module_files.txt
done

echo "Files combined into module_files.txt"