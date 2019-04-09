#!/bin/bash

# Adapter from GECKO/GetCSB output to Chromeister output format, with the species name and chromosome
# $1: Input file
# $2: Output file
# $3: Species X name (5 chars)
# $4: Species Y name (5 chars)
# $5: Species X chromosome
# $6: Species Y chromosome

head -n 16 $1 > ./header_file.txt
tail -n +17 $1 > ./frags_file.csv
python3 block_tracer_file_adapter.py ./header_file.txt ./frags_file.csv
rm header_file.txt
rm frags_file.csv
echo $3","$4","$5","$6 > $2
cat length_file.txt output_df.csv >> $2
echo "0,0,0,0,0,Null event" >> $2
rm length_file.txt
rm output_df.csv