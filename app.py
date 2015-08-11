#!/usr/bin/env python

import sys
import pprint
import sqlite3

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
	# dist = {}
	# pred = {}

	conn = sqlite3.connect("mydatabase.db")
	cursor = conn.cursor()

	for u in adjacency_list:
		# dist[u] = {}
		# pred[u] = {}
		for v in adjacency_list:
			# dist[u][v] = -1501
			cursor.execute("insert into dist values (?, ?, ?)", (u, v, -9999999))
			
			# pred[u][v] = -1
			cursor.execute("insert into pred values (?, ?, ?)", (u, v, ""))

			# cursor.execute("select count(*) from dist")
			# print cursor.fetchone()

		# dist[u][u] = 0
		cursor.execute("insert into dist values (?, ?, ?)", (u, u, 0))

		for neighbor in adjacency_list[u]:
			# dist[u][neighbor] = 1
			cursor.execute("update dist set from_node=?, to_node=?, dist=? where from_node=? and to_node=?", (u, neighbor, 1, u, neighbor))

			# pred[u][neighbor] = u
			cursor.execute("update pred set from_node=?, to_node=?, pred_node=? where from_node=? and to_node=?", (u, neighbor, u, u, neighbor))

	# pp.pprint(pred)

	conn.commit()
	conn.close()

def inverse_floyd_warshall(adjacency_list):
	conn = sqlite3.connect("mydatabase.db")
	cursor = conn.cursor()

	for t in adjacency_list:
		# given dist u to v, check if path u - t - v is longer
		for u in adjacency_list:
			for v in adjacency_list:

				cursor.execute("select dist from dist where from_node=? and to_node=? limit 1", (u, t))
				dist_u_t = cursor.fetchone()[0]

				cursor.execute("select dist from dist where from_node=? and to_node=? limit 1", (t, v))
				dist_t_v = cursor.fetchone()[0]

				cursor.execute("select dist from dist where from_node=? and to_node=? limit 1", (u, v))
				dist_u_v = cursor.fetchone()[0]

				newdist = dist_u_t + dist_t_v

				if newdist > dist_u_v:
					cursor.execute("update dist set dist_u_v=? where from_node=? and to_node=?", (newdist, u, v))

					cursor.execute("select pred_node from pred where from_node=? and to_node=? limit 1", (t, v))
					pred_t_v = cursor.fetchone()[0]

					cursor.execute("update pred set pred_node=? where from_node=? and to_node=?", (pred_t_v, u, v))

					# dist[u][v] = newdist
					# pred[u][v] = pred[t][v] # route new path through t
					conn.commit()
	
	conn.close()
	# return dist, pred

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

def init_database(adjacency_list):
	conn = sqlite3.connect("mydatabase.db")
	cursor = conn.cursor()

	cursor.execute("DROP TABLE IF EXISTS dist")
	cursor.execute("DROP TABLE IF EXISTS pred")

	cursor.execute("""CREATE TABLE dist
                 (from_node text, to_node text, dist integer)
              """)

	cursor.execute("""CREATE TABLE pred
                 (from_node text, to_node text, pred_node text)
              """)

	conn.commit()
	conn.close()

input_text = read_input()
matrix = create_graph_matrix(input_text)
adjacency_list = populate_adjacency_list(matrix)
init_database(adjacency_list)
init_floyd_warshall(adjacency_list)
inverse_floyd_warshall(adjacency_list)
# find_longest_distance(adjacency_list, dist, pred, matrix)
