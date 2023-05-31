#!/bin/sh
for f in consensuses-*.xz
do
    echo "Moving and expanding file: $f"
    mv -i $f consensuses
    cd consensuses
    unxz $f
    tar xvf $(basename $f .xz)
    cd ..
done
