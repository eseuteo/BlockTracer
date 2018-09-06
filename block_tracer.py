import argparse

def obtain_blocks(file):
    events = []
    file_events = [line.rstrip('\n') for line in open(file)]
    length_x = int(file_events[0].split(',')[0])
    length_y = int(file_events[0].split(',')[1])
    temp_list = file_events[2:-1]
    for line in temp_list:
        event = line.split(",")
        for i in range(4):
            if i % 2 == 0:
                event[i] = str(int(int(event[i]) * length_x / 1000))
            else:
                event[i] = str(int(int(event[i]) * length_y / 1000))
        if int(event[0]) > int(event[2]):
            event[0], event[2] = event[2], event[0]
        events.append(event)
    return events

def compare_blocks(base_block, new_blocks_list):
    blocks = []
    for block in new_blocks_list:
        if overlapped(base_block, block):
            if percentage_overlapped(base_block, block) > 80:
                # Update block (only the part overlapped)
                blocks.append(block)
    return blocks
    
# Think of a way to make it non-strict (?)
def overlapped(block_a, block_b):
    return int(block_a[1]) <= int(block_b[2]) and int(block_b[0]) <= int(block_a[3])

def percentage_overlapped(block_a, block_b):
    x1 = int(block_a[1])
    x2 = int(block_a[3])
    y1 = int(block_b[0])
    y2 = int(block_b[2])
    return 100 * (min(x2, y2) - max(x1, y1)) / min(x2-x1, y2-y1)

def get_comparison_name(path):
    path = path.split('/')
    return path[-1]

def recursive_overlap_checking(files, index, current_blocks, report, name, min_depth):
    if index >= min_depth:
        for block in current_blocks:
            print(report + name + '\t' + str(block) + '\n')
    if index < len(files):
        new_comparison_blocks = obtain_blocks(files[index])
        new_name = get_comparison_name(files[index])
        for block in current_blocks:
            new_blocks = compare_blocks(block, new_comparison_blocks)
            if new_blocks != []:
                recursive_overlap_checking(files, index + 1, new_blocks, report + name + '\t' + str(block) + '\n', new_name, min_depth)
        
parser = argparse.ArgumentParser(description='Process chromeister csv in order to find coincidences.')
parser.add_argument('input_filename', type = str, nargs = 1, help = 'Input filename containing paths to matrix files')
parser.add_argument('--min_depth', default = -1, type = int, nargs = 1, help = 'Blocks minimum depth. Default value is the number of filenames in the input file.')
args = parser.parse_args()

input_filename = args.input_filename[0]
min_depth = args.min_depth[0]

files = [line.rstrip('\n') for line in open(input_filename)]
if min_depth == -1:
    min_depth = len(files)
index = 0
current_blocks = obtain_blocks(files[0])
recursive_overlap_checking(files, index + 1, current_blocks, '', get_comparison_name(files[0]), min_depth)