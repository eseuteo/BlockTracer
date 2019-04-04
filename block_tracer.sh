#!/bin/bash
# $1 input files folder
# $2 output files folder
# $3 min depth

pwd
./block_tracer_file_adapter.sh $1
python3 block_tracer.py "bt_"$1 traced_blocks.csv --min_depth $3
mv $traced_blocks.csv $2

# # $1 input files folder
# # $2 output files folder
# # $3 min depth

# for file in $(ls $1); do  
# 	echo $1$file
# 	if [ -z $3 ] # If a tree depth is not given
# 		then
# 			python3 block_tracer.py $1$file $file.csv	
# 		exit 1
# 	fi
# 	python3 block_tracer.py $1$file $file.csv --min_depth $3
# 	mv $file.csv $2
# done
# find ./$2 -name "*.csv" -size -37c -delete
