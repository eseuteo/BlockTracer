# BlockTracer
A tool for tracing DNA __blocks__ along several species. It was created as part of a computational workflow, to be used with [Gecko][1] and [Chromeister][2]. The idea beneath this python script is to use the block's coordinates in order to find overlapping regions.

# Requirements
In order to run this Python script you will need to have Python (version 3.6 or higher) installed in your computer. There are no additional requirements.

# Usage
BlockTracer uses three input parameters, and the output is one single comma separated values (CSV) file. The input arguments are:
* input_filename: The absolute path of the input file, whose characteristics are described below.
* output_filename: The absolute path of the output CSV file
* min_depth: The minimum depth for a traced block to be taken into account. This element is described below.

The __input_filename__ argument will be the path of a file containing CSV files concatenated, containing the blocks found in different comparisons. The comparisons have to be linked and related (i.e.: If you want to find shared blocks between species A, B and C, the input file should have the blocks between __A and B__ and between __B and C__).

The __min_depth__ argument is set depending on the _strictness_ wanted for the BlockTracer. Let's say the user has the linked and related comparisons between 7 species, but he or she wants to find blocks traced throughout at least 5 species. Then the min_depth parameter will be set to 5 and all those blocks traced with a depth of 5 or higher will be returned.
In order to execute this script, it has to be run with python with the following command:

```python3 block_tracer.py <input_filename> <output_filename> --min_depth <min_depth>```



[1]:https://github.com/estebanpw/gecko
[2]:https://github.com/estebanpw/chromeister

