#!/bin/bash

for file in $(ls $1); do
	echo $file >> $2  
	if [ -z $3 ]
		then
			python3 block_tracer.py $1$file >> $2	
		exit 1
	fi
	python3 block_tracer.py $1$file --min_depth $3 >> $2
done
