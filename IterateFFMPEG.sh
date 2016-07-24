#!/bin/sh

#  IterateFFMPEG.sh
#  
#
#  Created by Robert Henden on 7/23/16.
#

for F in $@
do

    echo "Processing $F"
    ffmpeg -i "$F" -ar 22050 -ac 1 "$F".wav

done