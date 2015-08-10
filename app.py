#!/usr/bin/env python

import sys
import pprint

pp = pprint.PrettyPrinter(indent=4)

NO_EDGE_WEIGHT = 0

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

	return adjacencyDict


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

def init_floyd_warshall(adjacency_list):
	dist = {}
	pred = {}

	for u in adjacency_list:
		dist[u] = {}
		pred[u] = {}
		for v in adjacency_list:
			dist[u][v] = -999999
			pred[u][v] = -1
		dist[u][u] = 0
		for neighbor in adjacency_list[u]:
			dist[u][neighbor] = 1
			pred[u][neighbor] = u

	return dist, pred

def inverse_floyd_warshall(adjacency_list, dist, pred):
	for t in adjacency_list:
		# given dist u to v, check if path u - t - v is longer
		for u in adjacency_list:
			for v in adjacency_list:
				newdist = dist[u][t] + dist[t][v]
				if newdist > dist[u][v]:
					dist[u][v] = newdist
					pred[u][v] = pred[t][v] # route new path through t

	return dist, pred

def find_longest_distance(adjacency_list, dist, pred, matrix):

	longest_routes = {}
	longest_distance = 0;

	for u in dist:
		for v in dist[u]:
			if dist[u][v] >= longest_distance:
				longest_distance = dist[u][v]

	for u in dist:
		for v in dist[u]:
			if dist[u][v] == longest_distance:
				# starts at u, ends at v
				getPath(pred,u,v, matrix)
				print ''

def getPath(pred, start, end, matrix):

	if start == end:
		print matrix[int(start.split(' ',1)[0])][int(start.split(' ',1)[1])]
	elif pred[start][end] < 0:
		print "Path does not exist"
	else:
		getPath(pred, start, pred[start][end], matrix)
		print matrix[int(end.split(' ',1)[0])][int(end.split(' ',1)[1])]

input_text = read_input()
matrix = create_graph_matrix(input_text)
adjacency_list = populate_adjacency_list(matrix)
dist, pred = init_floyd_warshall(adjacency_list)
dist, pred = inverse_floyd_warshall(adjacency_list, dist, pred)
find_longest_distance(adjacency_list, dist, pred, matrix)
