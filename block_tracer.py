import argparse
import copy

# Class for making linked list of blocks (the traced and related blocks)
class TracedBlock:
    def __init__(self, x_species, x_chromosome, x_len, x1, x2, y_species, y_chromosome, y_len, y1, y2, report = ""):
        self.x_species = x_species
        self.x_chromosome = x_chromosome
        self.x_len = x_len
        self.x1 = min(x1, x2)
        self.x2 = max(x1, x2)
        self.y_species = y_species
        self.y_chromosome = y_chromosome
        self.y_len = y_len
        self.y1 = min(y1, y2)
        self.y2 = max(y1, y2)
        self.report = report

# Obaining the line of text to be included in the csv
def get_block_csv(b):
    return f"{b.x_species},{b.x_chromosome},{b.x1},{b.x2},{b.y_species},{b.y_chromosome},{b.y1},{b.y2}"

# Obtaining the species names
def obtain_names(b):
    return b[0], b[2]

# Obtaining the species chromosomes
def obtain_chromosomes(b):
    return b[1], b[3]

# Obtaining overlap coefficient
def overlap_coefficient(block_a, block_b):
    x1 = block_a.y1
    x2 = block_a.y2
    y1 = block_b.x1
    y2 = block_b.x2
    if (min(x2, y2) < max (x1, y1)):
        return 0 #not overlaped
    return 100 * (min(x2, y2) - max(x1, y1)) / min(x2-x1, y2-y1)

# Obtaining comparison name from path
def get_comparison_name(path):
    path = path.split('/')
    return path[-1]

# Obtain blocks available in a comparison file
def obtain_blocks(file, index):
    events = []
    file_events = file.split('\n')
    species_x = file_events[0].split(',')[0]
    chromosome_x = file_events[0].split(',')[1]
    species_y = file_events[0].split(',')[2]
    chromosome_y = file_events[0].split(',')[3]
    length_x = int(file_events[1].split(',')[0])
    length_y = int(file_events[1].split(',')[1])
    event_list = file_events[3:-2]
    for line in event_list:
        event = line.split(",")
        event.append(length_x)
        event.append(length_y)
        event.append([species_x, chromosome_x, species_y, chromosome_y])
        event[0], event[1], event[2], event[3] = int(event[0]), int(event[1]), int(event[2]), int(event[3])
        current_traced_block = TracedBlock(species_x, chromosome_x, length_x, int(event[0]), int(event[2]), species_y, chromosome_y, length_y, int(event[1]), int(event[3]))
        current_traced_block.report = (str(vars(current_traced_block)))
        events.append(current_traced_block)
        # print(vars(current_traced_block))
        del current_traced_block
    return events

# Determine if the overlap coefficient is higher than a certain threshold
def related(block_a, block_b):
    return overlap_coefficient(block_a, block_b) > 50

def merge_blocks(block_a, block_b):
    new_block = copy.deepcopy(block_b)
    new_block.report = ''
    new_block.report = block_a.report + "APPEND" + str(vars(new_block))
    new_block.x1 = max(block_a.y1, block_b.x1)
    new_block.x2 = min(block_a.y2, block_b.x2)
    new_block.y_len = block_b.y_len
    return new_block

def adapt(block_a, i):
    return str(i) + "," + block_a['x_species']+ "," + block_a['x_chromosome']+ "," + str(block_a['x1'])+ "," + str(block_a['x2'])+ "," + block_a['y_species']+ "," + block_a['y_chromosome']+ "," + str(block_a['y1'])+ "," + str(block_a['y2'])

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
files = []
current_file = ""
with open(input_filename, 'r') as ifn:
    line = ifn.readline()
    while(line):
        if 'Null event' in line:
            current_file += line
            files.append(current_file)
            current_file = ""
        else:
            current_file += line
        line = ifn.readline()

list_of_list_of_blocks = []
i = 0
for file in files:
    list_of_blocks = obtain_blocks(file, i)
    list_of_list_of_blocks.append(list_of_blocks)
    i += 1

j=0
print("Block,SpeciesX,ChromosomeX,StartX,EndX,SpeciesY,ChromosomesY,StartY,EndY")

while len(list_of_list_of_blocks) > 1:
    list_a = list_of_list_of_blocks.pop(0)
    list_b = list_of_list_of_blocks.pop(0)
    list_c = []

    for block_a in list_a:
        blocks = block_a.report.split("APPEND")
        if len(blocks) > min_depth:
            for block in blocks:
                new_one = eval(block)
                new_line = adapt(new_one, j)
                print(new_line)
            j += 1

    if len(list_a) < 1:
        break
    for block_a in list_a:
        for block_b in list_b:
            if related(block_a, block_b):
                new_block = copy.deepcopy(block_b)
                new_block.report = ''
                new_block.report = block_a.report + "APPEND" + str(vars(new_block))
                new_block.x1 = max(block_a.y1, block_b.x1)
                list_c.append(new_block)
    list_of_list_of_blocks.insert(0, list_c)

for block_a in list_of_list_of_blocks[0]:
    blocks = block_a.report.split("APPEND")
    for block in blocks:
        new_one = eval(block)
        new_line = adapt(new_one, j)
        print(new_line)
    j += 1
