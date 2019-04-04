import argparse
import copy

class traced_block:
    def __init__(self, x_species, y_species, x1, x2, y1, y2, next = None):
        self.x_species = x_species
        self.y_species = y_species
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.next = next

def check_inversion(event):
    if event[0] > event[2]:
        event[0], event[2] = event[2], event[0]
    if event[1] > event[3]:
        event[1], event[3] = event[3], event[1]
    return event

def overlapped(block_a, block_b):
    return int(block_a[1]) <= int(block_b[2]) and int(block_b[0]) <= int(block_a[3])

def overlap_coefficient(block_a, block_b):
    x1 = int(block_a[0])
    x2 = int(block_a[2])
    y1 = int(block_b[1])
    y2 = int(block_b[3])
    if (min(x2, y2) < max (x1, y1)):
        return 0 #not overlaped
    return 100 * (min(x2, y2) - max(x1, y1)) / min(x2-x1, y2-y1)

def get_comparison_name(path):
    path = path.split('/')
    return path[-1]

def scale(block):
    new_block = copy.deepcopy(block)
    for i in range(5):
        length_index = 6 if i % 2 == 1 or i == 4 else 7
        new_block[i] = str(int(int(block[i]) / block[length_index] * 1000))
    return new_block

def unscale(block):
    new_block = copy.deepcopy(block)
    for i in range(5):
        length_index = 6 if i % 2 == 1 or i == 4 else 7
        new_block[i] = int(int(block[i]) * block[length_index] / 1000)
    return new_block

def obtain_blocks(file, index, name):
    events = []
    file_events = [line.rstrip('\n') for line in open(file)]
    length_x = int(file_events[0].split(',')[0])
    length_y = int(file_events[0].split(',')[1])
    event_list = file_events[2:-1]
    for line in event_list:
        event = line.split(",")
        #event = check_inversion(event)
        event.append(length_x)
        event.append(length_y)
        event.append(name)
        event = unscale(event)
        events.append(event)
    return events

def compare_blocks(base_block, new_blocks_list):
    blocks = []
    original_blocks = []
    for block in new_blocks_list:
        original_block = copy.deepcopy(block)
        if overlap_coefficient(base_block, block) > 80:
            # Take only the overlapped part
            if int(base_block[1]) > int(block[0]):
                block[1] = str(int(block[1]) + ((int(base_block[1]) - int(block[0]))*block[7]//block[6]))
                block[0] = base_block[1]
            if int(base_block[3]) < int(block[2]):
                block[3] = str(int(block[3]) - ((int(block[2]) - int(base_block[3]))*block[7]//block[6]))
                block[2] = base_block[3]
            # Blocks that are inversions of inverted transposition need y coordinates to be swapped
            if 'inv' in block[5]:
                block[1], block[3] = block[3], block[1]
                original_block[1], original_block[3] = original_block[3], original_block[1]
            block[4] = abs(int(block[1]) - int(block[3]))
            blocks.append(block)
            original_blocks.append(original_block)
    return blocks, original_blocks

def recursive_overlap_checking(files, index, current_blocks, current_original_blocks, output_file, traced_block_info, min_depth):
    if index >= min_depth:
        for i in range(len(current_blocks)):
            output_file += str(traced_block_info)
            output_file += (str(index-1) + '\t' + str(scale(current_blocks[i])[:-1]) + '\t' + str(scale(current_original_blocks[i])[:-1]) + '\n\n')
            print(output_file)
    if index < len(files):
        new_name = get_comparison_name(files[index])
        new_comparison_blocks = obtain_blocks(files[index], index, new_name)
        for i in range(len(current_blocks)):
            new_blocks, new_original_blocks = compare_blocks(current_blocks[i], new_comparison_blocks)
            if new_blocks != []:
                return recursive_overlap_checking(files, index + 1, new_blocks, new_original_blocks, output_file, traced_block_info + str(index-1) + '\t' + str(scale(current_blocks[i])[:-1]) + '\t' + str(scale(current_original_blocks[i])[:-1]) + '\n', min_depth)
    else:
        print(output_file)
        return output_file

def related(block_a, block_b):
    return overlap_coefficient(block_a, block_b) > 95

def is_inverted(block):
    return block[0] < block[2]

def take_overlapping_part(block_a, block_b):
    new_block = copy.deepcopy(block_b)
    scale_index = 0; factor = 1
    if is_inverted(new_block):
        scale_index = scale_index+2
        factor = -1*factor
    # Left Edge
    lb1 = block_b[3] - block_b[1]
    lb2 = block_b[2] - block_b[0]
    if block_a[0] > block_b[1]:
        d1 = block_a[0] - block_b[1]
        scaling = int(d1 * lb2 / lb1)
        new_block[0+scale_index] = block_b[0 + scale_index] + factor * scaling
        new_block[1] = block_b[0]
    # Right Edge
    if block_a[2] < block_b[3]:
        d2 = block_b[3] - block_a[2]
        scaling = int( d2 * lb2 / lb1 )
        new_block[2-scale_index] = block_b[2 - scale_index] - factor * scaling
        new_block[3] = block_a[2]
    new_block[-1] = block_b[-1]
    return new_block
     
parser = argparse.ArgumentParser(description='Process chromeister csv in order to find coincidences.')
parser.add_argument('input_filename', type = str, nargs = 1, help = 'Input filename containing paths to matrix files')
parser.add_argument('output_filename', type = str, nargs = 1, help = 'Output filename')
parser.add_argument('--min_depth', default = -1, type = int, nargs = 1, help = 'Blocks minimum depth. Default value is the number of filenames in the input file.')
args = parser.parse_args()

input_filename = args.input_filename[0]
output = args.output_filename[0]
min_depth = args.min_depth[0]

output_file = open(output, 'w')
output_file.write('Species\tChromosome\tStart\tEnd\tLength\n')

files = [line.rstrip('\n') for line in open(input_filename)]
current_blocks = obtain_blocks(files[0], 0, get_comparison_name(files[0]))

list_of_list_of_blocks = []
i = 0
for file in files:
    list_of_blocks = obtain_blocks(file, i, get_comparison_name(file))
    list_of_list_of_blocks.append(list_of_blocks)
    i += 1

list_storage = []
list_storage.append(list_of_list_of_blocks)
current_list_len = len(list_of_list_of_blocks)
    
while current_list_len > 1:
    i = 0
    new_list_of_list_of_blocks = []
    while i < len(list_of_list_of_blocks) - 1:
        list_of_blocks_a = list_of_list_of_blocks[i]
        list_of_blocks_b = list_of_list_of_blocks[i+1]
        resulting_list_of_blocks = []
        for block_a in list_of_blocks_a:
            for block_b in list_of_blocks_b:
                if related(block_a, block_b):
                    new_block = take_overlapping_part(block_a, block_b)
                    resulting_list_of_blocks.append(new_block)
        new_list_of_list_of_blocks.append(resulting_list_of_blocks)
        i += 1
    list_storage.append(new_list_of_list_of_blocks)
    list_of_list_of_blocks = new_list_of_list_of_blocks
    current_list_len = len(list_of_list_of_blocks)

for list_of_lists in list_storage:
    for list_of_blocks in list_of_lists:
        for block in list_of_blocks:
            print(scale(block))
    print("\n")
print('---')
    
            


