#!/bin/bash

head -n 16 $1 > ./header_file.txt
tail -n +17 $1 > ./frags_file.csv
python3 block_tracer_file_adapter.py ./header_file.txt ./frags_file.csv
rm header_file.txt
rm frags_file.csv
cat length_file.txt output_df.csv > $2
echo "0,0,0,0,0,Null event" >> $2
rm length_file.txt
rm output_df.csv