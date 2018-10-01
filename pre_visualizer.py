import argparse
import copy
import pandas as pd
import ast

def unscale(block):
    new_block = copy.deepcopy(block)
    for i in range(5):
        length_index = 7 if i % 2 == 1 or i == 4 else 6
        new_block[i] = str(int(int(block[i]) * block[length_index] / 1000))
    return new_block

def check_inversion(event):
    if int(event[0]) > int(event[2]):
        event[0], event[2] = event[2], event[0]
    return event

def obtain_blocks(file):
    events = []
    file_events = [line.rstrip('\n') for line in open(file)]
    length_x = int(file_events[0].split(',')[0])
    length_y = int(file_events[0].split(',')[1])
    event_list = file_events[2:-1]
    for line in event_list:
        event = line.split(",")
        event = check_inversion(event)
        event.append(length_x)
        event.append(length_y)
        event = unscale(event)
        events.append(event)
    return events

def obtain_max_length(comparisons):
    max_length = 0
    for comparison in comparisons:
        file_events = [line.rstrip('\n') for line in open(comparison)]
        length_x = int(file_events[0].split(',')[0])
        length_y = int(file_events[0].split(',')[1])
        max_length = max(max_length, length_x, length_y)
    return max_length

parser = argparse.ArgumentParser(description='Generate csv for block tracer visualizer.')
parser.add_argument('input_comparisons_filename', type = str, nargs = 1, help = 'Input filename containing paths to chromeister comparisons')
parser.add_argument('input_blocktracer_filename', type = str, nargs = 1, help = 'Block tracer output')
parser.add_argument('output_visualizer_filename', type = str, nargs = 1, help = 'Output filename for the visualizer')
args = parser.parse_args()

comparisons_filename = args.input_comparisons_filename[0]
blocks_filename = args.input_blocktracer_filename[0]
output_filename = args.output_visualizer_filename[0]

comparisons = [line.rstrip('\n') for line in open(comparisons_filename)]
max_length = obtain_max_length(comparisons)
num_syn = 0
output_file_0 = open(output_filename + '0', 'w')
output_file_0.write("bID\tini\tfin\tlong\tgen\tsyn\n")
for i in range(len(comparisons)):
    output_file_0 = open(output_filename + str(i), 'a')
    output_file_1 = open(output_filename + str(i+1), 'a')
    #output_file_0.write("bID\tini\tfin\tlong\tgen\tsyn\n")
    output_file_1.write("bID\tini\tfin\tlong\tgen\tsyn\n")
    comparison_blocks = obtain_blocks(comparisons[i])
    for block in comparison_blocks:
        ini_0 = int(block[0]) * 1000 // max_length
        fin_0 = int(block[2]) * 1000 // max_length
        len_0 = fin_0 - ini_0
        ini_1 = int(block[1]) * 1000 // max_length
        fin_1 = int(block[3]) * 1000 // max_length
        len_1 = fin_1 - ini_1
        output_file_0.write(str(i) + '\t' + str(ini_0) + '\t' + str(fin_0) + '\t' + str(len_0) + '\t' + str(i) + '\t' + str(num_syn) + '\n')
        output_file_1.write(str(i) + '\t' + str(ini_1) + '\t' + str(fin_1) + '\t' + str(len_1) + '\t' + str(i) + '\t' + str(num_syn) + '\n')
        num_syn += 1

df = pd.read_csv(blocks_filename, sep='\t')
file_IDs = df['file_ID']
blocks = df['traced_block']
for i in range(len(blocks)):
    file_ID = file_IDs[i]
    if file_ID == 0:
        num_syn += 1
    block = ast.literal_eval(blocks[i])
    block = unscale(block)
    output_file_0 = open(output_filename + str(file_ID), 'a')
    output_file_1 = open(output_filename + str(file_ID + 1), 'a')
    ini_0 = int(block[0]) * 1000 // max_length
    fin_0 = int(block[2]) * 1000 // max_length
    len_0 = fin_0 - ini_0
    ini_1 = int(block[1]) * 1000 // max_length
    fin_1 = int(block[3]) * 1000 // max_length
    len_1 = fin_1 - ini_1
    output_file_0.write(str(i) + '\t' + str(ini_0) + '\t' + str(fin_0) + '\t' + str(len_0) + '\t' + '1000' + '\t' + str(num_syn) + '\n')
    output_file_1.write(str(i) + '\t' + str(ini_1) + '\t' + str(fin_1) + '\t' + str(len_1) + '\t' + '500' + '\t' + str(num_syn) + '\n')


