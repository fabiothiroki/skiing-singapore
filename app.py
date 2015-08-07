#!/usr/bin/env python

import sys

with open(sys.argv[1], 'r') as my_file:
	str_first_line = my_file.readline().strip()
	arr_first_line = str_first_line.split(' ', 1 )

	num_lines = arr_first_line[0]
	num_columns =  arr_first_line[1]

	print num_lines, num_columns

	inputText = (my_file.read())

