import argparse
import copy

def append_block_to_file(index, block):
    file = open('output' + str(index), 'a')
    new_line = str(index) + '\t' + str(block[0]) + '\t' + block(block[2]) + '\t' + str(int(block[2]) - int(block[0])) + '\t' + '0' + '\t' + '0' + '\n'

def obtain_blocks(file, index, name):
    events = []
    file_events = [line.rstrip('\n') for line in open(file)]
    length_x = int(file_events[0].split(',')[0])
    length_y = int(file_events[0].split(',')[1])
    temp_list = file_events[2:-1]
    for line in temp_list:
        event = line.split(",")
        # Inversion!
        if int(event[0]) > int(event[2]):
            event[0], event[2] = event[2], event[0]
        for i in range(4):
            if i % 2 == 0:
                event[i] = str(int(int(event[i]) * length_x / 1000))
            else:
                event[i] = str(int(int(event[i]) * length_y / 1000))
        event[4] = str(int(int(event[4]) * length_y / 1000))
        event.append(length_x)
        event.append(length_y)
        event.append(name)
        events.append(event)
    return events

def compare_blocks(base_block, new_blocks_list):
    blocks = []
    original_blocks = []
    for block in new_blocks_list:
        original_block = copy.deepcopy(block)
        if overlapped(base_block, block):
            if overlap_coefficient(base_block, block) > 60:
                if int(base_block[1]) > int(block[0]):
                    block[1] = str(int(block[1]) + ((int(base_block[1]) - int(block[0]))*block[7]//block[6]))
                    block[0] = base_block[1]
                if int(base_block[3]) < int(block[2]):
                    block[3] = str(int(block[3]) - ((int(block[2]) - int(base_block[3]))*block[7]//block[6]))
                    block[2] = base_block[3]
                block[4] = int(block[2]) - int(block[0])
                # print(original_block)
                # print(block)
                blocks.append(block)
                original_blocks.append(original_block)
    return blocks, original_blocks
    
def overlapped(block_a, block_b):
    return int(block_a[1]) <= int(block_b[2]) and int(block_b[0]) <= int(block_a[3])

def overlap_coefficient(block_a, block_b):
    x1 = int(block_a[1])
    x2 = int(block_a[3])
    y1 = int(block_b[0])
    y2 = int(block_b[2])
    return 100 * (min(x2, y2) - max(x1, y1)) / min(x2-x1, y2-y1)

def get_comparison_name(path):
    path = path.split('/')
    return path[-1]

def scale(block):
    for i in range(4):
        length_index = 7 if i % 2 == 1 or i == 4 else 6
        block[i] = str(int(int(block[i]) / block[length_index] * 1000))
    return block

def recursive_overlap_checking(files, index, current_blocks, current_original_blocks, output_file, traced_block_info, min_depth):
    if index >= min_depth:
        # if index >= len(files) - 1:
        #     for i in range(len(current_blocks)):
                # print(block)
                # print('+++')
                # print(current_blocks[i])
                # print('---')
                # print(current_original_blocks[i])
                # print('***')
                # print(scaled_block)
                # block[1] = 
                # block[3] = 
        for i in range(len(current_blocks)):
            output_file.write(traced_block_info)
            output_file.write(current_blocks[i][-1] + '\t' + str(scale(current_blocks[i])[:-3]) + '\t' + str(scale(current_original_blocks[i])[:-3]) + '\n\n')
    if index < len(files):
        new_name = get_comparison_name(files[index])
        new_comparison_blocks = obtain_blocks(files[index], index, new_name)
        for i in range(len(current_blocks)):
            new_blocks, new_original_blocks = compare_blocks(current_blocks[i], new_comparison_blocks)
            if new_blocks != []:
                recursive_overlap_checking(files, index + 1, new_blocks, new_original_blocks, output_file, traced_block_info + current_blocks[i][-1] + '\t' + str(scale(current_blocks[i])[:-3]) + '\t' + str(scale(current_original_blocks[i])[:-3]) + '\n', min_depth)

# Arguments parsing        
parser = argparse.ArgumentParser(description='Process chromeister csv in order to find coincidences.')
parser.add_argument('input_filename', type = str, nargs = 1, help = 'Input filename containing paths to matrix files')
parser.add_argument('output_visualizer_filename', type = str, nargs = 1, help = 'Output filename for the visualizer')
parser.add_argument('--min_depth', default = -1, type = int, nargs = 1, help = 'Blocks minimum depth. Default value is the number of filenames in the input file.')
args = parser.parse_args()

input_filename = args.input_filename[0]
output = args.output_visualizer_filename[0]
min_depth = args.min_depth[0]
##

# 'Main'
files = [line.rstrip('\n') for line in open(input_filename)]
output_file = open(output, 'a')
output_file.write('file name\ttraced block\toriginal block\n')
if min_depth == -1:
    min_depth = len(files)
current_blocks = obtain_blocks(files[0], 0, get_comparison_name(files[0]))
# output_file.write(get_comparison_name(files[0]))
recursive_overlap_checking(files, 1, current_blocks, current_blocks, output_file, '', min_depth)
##