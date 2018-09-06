#!/bin/bash

for file in $(ls $1); do
	echo $file >> $2  
	python3 block_tracer.py $1$file asd >> $2
done
