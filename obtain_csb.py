import argparse
import pandas as pd
import sys
import numpy as np

def complete_colinearity(x_order, y_order, strand, i, j):
    return abs(x_order[i] - x_order[j]) == 1 and abs(y_order[i] - y_order[j]) == 1 and strand[i] == strand[j]

def complete_bi_colinearity(x_order, y_order, strand, i, j, k):
    return complete_colinearity(x_order, y_order, strand, i, j) and complete_colinearity(x_order, y_order, strand, j, k)

def get_start(frags, frag_set, axis, strand):
    if strand == 'r' and axis == 'y':
        start = -1
    else:
        start = sys.maxsize
    for index in frag_set:
        if strand == 'r' and axis == 'y':
            start = max(start, frags.iloc[index][axis + 'Start'])
        else:
            start = min(start, frags.iloc[index][axis + 'Start'])
    return start

def get_end(frags, frag_set, axis, strand):
    if strand == 'r' and axis == 'y':
        end = sys.maxsize
    else:
        end = -1
    for index in frag_set:
        if strand == 'r' and axis == 'y':
            end = min(end, frags.iloc[index][axis + 'End'])
        else:
            end = max(end, frags.iloc[index][axis + 'End'])
    return end

def obtain_csbs(frags):
    csbs = []
    current_csb = {}
    actual_id = frags[0]
    x_order = frags[1]
    y_order = frags[2]
    strand = frags[3]
    for i in range(len(actual_id) - 2):
        j = i + 1
        k = i + 2
        if complete_bi_colinearity(x_order, y_order, strand, i, j, k):
            if 'start' not in current_csb:
                current_csb['start'] = x_order[i]
            current_csb['end'] = x_order[k]
        else:
            if 'start' in current_csb:
                csbs.append(current_csb)
                current_csb = {}
    if 'start' in current_csb:
        current_csb['end'] = x_order[j]
        csbs.append(current_csb)
    return csbs

parser = argparse.ArgumentParser(description='Obtain Computational Synteny Blocks (CSB) from frags csv')
parser.add_argument('input_filename', type = str, nargs = 1, help = 'Input frags csv')
parser.add_argument('output_filename', type = str, nargs = 1, help = 'Output CSB filename')
args = parser.parse_args()

input_filename = args.input_filename[0]
output_filename = args.output_filename[0]

frags = pd.read_csv(input_filename, skiprows=14)

frags_ids = frags.index.values
frags_x_order = frags.sort_values(by='xStart').index.values
frags_y_order = frags.sort_values(by='yStart').index.values
frags_strand = frags['strand(f/r)'].values

frags_for_csb_obtaining = [frags_ids, frags_x_order, frags_y_order, frags_strand]

csb_sets = obtain_csbs(frags_for_csb_obtaining)

types = []
csb_x_start = []
csb_y_start = []
csb_x_end = []
csb_y_end = []
csb_strand = []

for csb_set in csb_sets:
    types.append('csb')
    csb_x_start.append(frags.iloc[csb_set['start']]['xStart'])
    csb_y_start.append(frags.iloc[csb_set['start']]['yStart'])
    csb_x_end.append(frags.iloc[csb_set['end']]['xEnd'])
    csb_y_end.append(frags.iloc[csb_set['end']]['yEnd'])
    csb_strand.append(frags.iloc[csb_set['start']]['strand(f/r)'])

csb = pd.DataFrame({
    'type': types,
    'x_start': csb_x_start,
    'y_start': csb_y_start,
    'x_end': csb_x_end,
    'y_end': csb_y_end,
    'strand': csb_strand
})

csb.to_csv(output_filename, index=False)


