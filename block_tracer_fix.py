import argparse
import copy

class TracedBlock:
    def __init__(self, x_species, x_chromosome, x1, x2, y_species, y_chromosome, y1, y2, next = None):
        self.x_species = x_species
        self.x_chromosome = x_chromosome
        self.x1 = x1
        self.x2 = x2
        self.y_species = y_species
        self.y_chromosome = y_chromosome
        self.y1 = y1
        self.y2 = y2
        self.next = next

    def get_last(self):
        if self.next is None:
            return self
        else:
            return self.next.get_last()
    
    def get_length(self):
        length = 1
        if self.next is None:
            return length
        else:
            return self.next.get_length() + 1

def get_block_csv(b):
    return f"{b.x_species},{b.x_chromosome},{b.x1},{b.x2},{b.y_species},{b.y_chromosome},{b.y1},{b.y2}"

def obtain_names(filename):
    _filename = filename.split('-')
    return _filename[0][0:5], _filename[1][0:5]

def obtain_chromosomes(filename):
    _filename = filename.split('-')
    return _filename[0].split('.')[2], _filename[1].split('.')[2]

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

def obtain_blocks(file, index, name):
    events = []
    file_events = [line.rstrip('\n') for line in open(file)]
    length_x = int(file_events[0].split(',')[0])
    length_y = int(file_events[0].split(',')[1])
    event_list = file_events[2:-1]
    for line in event_list:
        event = line.split(",")
        event.append(length_x)
        event.append(length_y)
        event.append(name)
        event[0], event[1], event[2], event[3] = int(event[0]), int(event[1]), int(event[2]), int(event[3])
        events.append(event)
    return events

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

###########################
#   Block Tracer Main     #
###########################

# Argument parsing     
parser = argparse.ArgumentParser(description='Process chromeister csv in order to find coincidences.')
parser.add_argument('input_filename', type = str, nargs = 1, help = 'Input filename containing paths to matrix files')
parser.add_argument('output_filename', type = str, nargs = 1, help = 'Output filename')
parser.add_argument('--min_depth', default = -1, type = int, nargs = 1, help = 'Blocks minimum depth. Default value is the number of filenames in the input file.')
args = parser.parse_args()

input_filename = args.input_filename[0]
output = args.output_filename[0]
min_depth = args.min_depth[0]

# Obtain blocks available in every input file
files = [line.rstrip('\n') for line in open(input_filename)]
list_of_list_of_blocks = []
i = 0
for file in files:
    list_of_blocks = obtain_blocks(file, i, get_comparison_name(file))
    list_of_list_of_blocks.append(list_of_blocks)
    i += 1

# Create final list
list_storage = []
list_storage.append(list_of_list_of_blocks)
current_list_len = len(list_of_list_of_blocks)
    
# Check overlap between blocks
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

# Create actual traced blocks
# Firstly, the first element of the linked lists
traced_blocks_list = []
for list_of_blocks in list_storage[0]:
    for block in list_of_blocks:
        x_name, y_name = obtain_names(block[-1])
        x_chromosome, y_chromosome = obtain_chromosomes(block[-1])
        traced_blocks_list.append(TracedBlock(x_name, x_chromosome, block[1], block[3], y_name, y_chromosome, block[0], block[2]))

# Secondly, the linked lists are filled
i = 1
while (i < len(list_storage)):
    for list_of_blocks in list_storage[i]:
        for block in list_of_blocks:
            x_name, y_name = obtain_names(block[-1])
            x_chromosome, y_chromosome = obtain_chromosomes(block[-1])
            current_traced_block = TracedBlock(x_name, x_chromosome, block[1], block[3], y_name, y_chromosome, block[0], block[2])
            list_to_add_to_traced_blocks_list = []
            for traced_block in traced_blocks_list:
                last_block_traced = traced_block.get_last()
                if last_block_traced.y_species == current_traced_block.x_species:
                    list_to_add_to_traced_blocks_list.append(copy.deepcopy(traced_block))
                    last_block_traced.next = current_traced_block
            traced_blocks_list += list(set(list_to_add_to_traced_blocks_list))
    i += 1

# Filter regarding input min depth
traced_blocks_list = [x for x in traced_blocks_list if x.get_length() >= min_depth]

# Prepare csv lines and filter repeated traced blocks
i = 0
traced_blocks_set = set()
for traced_block in traced_blocks_list:
    current_block = traced_block
    text_for_traced_block = get_block_csv(current_block)
    text_for_traced_block += "\n"
    while not current_block.next is None:
        text_for_traced_block += get_block_csv(current_block.next)
        text_for_traced_block += "\n"
        current_block = current_block.next
    i += 1
    traced_blocks_set.add(text_for_traced_block)
    
# Write resulting traced blocks to output file
output_file = open(output, 'w')
output_file.write('Block,SpeciesX,ChromosomeX,StartX,EndX,SpeciesY,ChromosomesY,StartY,EndY\n')
i = 0
for element in traced_blocks_set:
    element = element.split('\n')
    element = element[:-1]
    for block in element:
        output_file.write(str(i) + ',' + block + '\n')
    i += 1
    
            


