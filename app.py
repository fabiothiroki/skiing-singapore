#!/usr/bin/env python

import sys
import pprint

pp = pprint.PrettyPrinter(indent=4)

def read_input():

	with open(sys.argv[1], 'r') as my_file:
		
		input_text = (my_file.read())

		return input_text

def create_graph_matrix(input_text):
	txt_lines = input_text.splitlines()
	arr_first_line = txt_lines[0].split(' ', 1 )

	num_lines = arr_first_line[0]
	num_columns = arr_first_line[1]

	matrix = []

	for line in range(1, int(num_lines)+1):
		current_line = txt_lines[line].split(' ', int(num_columns) - 1 )

		list_current_line = []

		for column in range (0, int(num_columns)):
			list_current_line.append(current_line[column])

		matrix.append(list_current_line)

	return matrix


def populate_adjacency_list(matrix):
	
	adjacencyDict = {}

	for line in range(0, len(matrix)):
		
		for column in range (0, len(matrix[0])):
			adjacencyDict[str(line) + ' ' + str(column)] = list_of_adjacent_nodes(matrix, line, column)

	pp.pprint(adjacencyDict)


def list_of_adjacent_nodes(matrix, line, column):
	adjacent_nodes = []

	if (line - 1 >= 0) and matrix[line - 1][column] < matrix[line][column]:
		adjacent_nodes.append(str(line - 1) + ' ' + str(column))

	if (column + 1 < len(matrix[0]) ) and matrix[line][column + 1] < matrix[line][column]:
		adjacent_nodes.append(str(line) + ' ' + str(column + 1))

	if (line + 1 < len(matrix) ) and matrix[line + 1][column] < matrix[line][column]:
		adjacent_nodes.append(str(line + 1) + ' ' + str(column))

	if (column - 1 >= 0) and matrix[line][column - 1] < matrix[line][column]:
		adjacent_nodes.append(str(line) + ' ' + str(column - 1))

	return adjacent_nodes

input_text = read_input()
matrix = create_graph_matrix(input_text)
populate_adjacency_list(matrix)

