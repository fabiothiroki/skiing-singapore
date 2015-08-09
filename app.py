#!/usr/bin/env python

import sys
import pprint

def read_input():

	with open(sys.argv[1], 'r') as my_file:
		
		inputText = (my_file.read())

		return inputText

def populateGraph(inputText):
	graphDict = {}
	pp = pprint.PrettyPrinter(indent=4)

	txt_lines = inputText.splitlines()
	arr_first_line = txt_lines[0].split(' ', 1 )

	num_lines = arr_first_line[0]
	num_columns = arr_first_line[1]

	for line in range(1, int(num_lines)):
		current_line = txt_lines[line].split(' ', int(num_columns) - 1 )
		
		for column in range (0, int(num_columns)):
			graphDict[ str(line) + ' ' + str(column)  ] = set()

	pp.pprint(graphDict)


inputText = read_input()
populateGraph(inputText)

