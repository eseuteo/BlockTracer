
import pandas as pd
import numpy as np
import argparse
import itertools

parser = argparse.ArgumentParser(description='Generate file from a CSB file with chromeister-like format')
parser.add_argument('header_filename', type=str, nargs=1, help='input CSB header filename')
parser.add_argument('csb_filename', type=str, nargs=1, help='input CSB csv filename')

args = parser.parse_args()
header_filename = args.header_filename[0]
csb_filename = args.csb_filename[0]

x_len = 0
y_len = 0

with open(header_filename, 'r') as header_file:
    for line in header_file:
        if 'SeqX length' in line:
            x_len = int(line.split()[3])
        if 'SeqY length' in line:
            y_len = int(line.split()[3])

df = pd.read_csv(csb_filename)
output_df = pd.concat([df['xStart'], df['yStart'], df['xEnd'], df['yEnd'], df['length'], df['diagonal']], axis = 1, keys = ['x1', 'y1', 'x2', 'y2', 'len', 'event'])

length_file = open("length_file.txt", "w")
length_file.write(f"{x_len},{y_len}\n")
length_file.close()
output_df.to_csv('output_df.csv', index = False) # Nombres si, index no



