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
    # print(base_block)
    for block in new_blocks_list:
        if overlapped(base_block, block):
            if percentage_overlapped(base_block, block) > 80:
                # print('\t', end = '')
                # print(block)
                blocks.append(block)
    return blocks
    
# Pensar en forma de que no sea estricto
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

def recursive_overlap_checking(files, index, current_blocks, report, name):
    if index >= len(files):
        for block in current_blocks:
            print(report + name + '\t' + str(block) + '\n')
    else:
        new_comparison_blocks = obtain_blocks(files[index])
        # for block in new_comparison_blocks:
        #     print(str(block))
        # print('_____')
        new_name = get_comparison_name(files[index])
        for block in current_blocks:
            new_blocks = compare_blocks(block, new_comparison_blocks)
            # print('||| Deciding whether to call the recursive function |||')
            # print(name)
            # print(block)
            # print(new_blocks)
            # print('|||||||||||||||||||||||||||||||||||||||||||||||||||||||')
            if new_blocks != []:
                # print('||||||||||||||||||| calling it ||||||||||||||||||||||||')
                recursive_overlap_checking(files, index + 1, new_blocks, report + name + '\t' + str(block) + '\n', new_name)
            # else:
                # print('||||||||||||||||||| not called ||||||||||||||||||||||||')
        
parser = argparse.ArgumentParser(description='Process chromeister matrices in order to find coincidences.')
parser.add_argument('input_filename', type = str, nargs = 1, help = 'input filename containing paths to matrix files')
parser.add_argument('output_filename', type = str, nargs = 1, help = 'output filename')
args = parser.parse_args()

input_filename = args.input_filename[0]
output_filename = args.output_filename[0]

files = [line.rstrip('\n') for line in open(input_filename)]
index = 0
current_blocks = obtain_blocks(files[0])
# for block in current_blocks:
#     print(str(block))
# print('_____')
recursive_overlap_checking(files, index + 1, current_blocks, '', get_comparison_name(files[0]))