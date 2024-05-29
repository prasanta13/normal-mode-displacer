#!/bin/bash

count=0
same_files=()

for i in {0..14}; do
    for ((j=i+1; j<=14; j++)); do
        echo "Comparing $i.xyz and $j.xyz"
        if diff -q "${i}.xyz" "${j}.xyz" > /dev/null; then
            echo "Files ${i}.xyz and ${j}.xyz are the same"
            count=$((count + 1))
            same_files+=("${i}.xyz and ${j}.xyz")
        fi
    done
done

echo "Total number of identical file pairs: $count"
echo "Identical file pairs:"
for pair in "${same_files[@]}"; do
    echo "$pair"
done

