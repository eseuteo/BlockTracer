#!/bin/bash

# Concatenates two files in one, separating them with three hyphens

cat $1 > $3"_"
cat $2 >> $3"_"
mv $3"_" $3