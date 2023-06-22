#!/usr/bin/env python3
# bfs.py

# Introduction to Algorithms, Fourth edition
# Linda Xiao and Tom Cormen

#########################################################################
#                                                                       #
# Copyright 2022 Massachusetts Institute of Technology                  #
#                                                                       #
# Permission is hereby granted, free of charge, to any person obtaining #
# a copy of this software and associated documentation files (the       #
# "Software"), to deal in the Software without restriction, including   #
# without limitation the rights to use, copy, modify, merge, publish,   #
# distribute, sublicense, and/or sell copies of the Software, and to    #
# permit persons to whom the Software is furnished to do so, subject to #
# the following conditions:                                             #
#                                                                       #
# The above copyright notice and this permission notice shall be        #
# included in all copies or substantial portions of the Software.       #
#                                                                       #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,       #
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF    #
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND                 #
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS   #
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN    #
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN     #
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE      #
# SOFTWARE.                                                             #
#                                                                       #
#########################################################################

from fifo_queue import Queue
from adjacency_list_graph import AdjacencyListGraph
from print_path import print_path

WHITE = 0  # undiscovered
GRAY = 1   # discovered
BLACK = 2  # visited


def bfs(G, source):
	"""Perform breadth-first search on a graph, filling in distances and predecessors.

	Arguments:
	G -- the graph, implemented with adjacency lists
	source -- index of the source vertex
	"""
	# Initialize all vertices to white with distance of infinity and no predecessor, except source is gray.
	card_V = G.get_card_V()  # vertices are numbered, so that color[i] gives the color of vertex i
	color = [WHITE] * card_V  # all unvisited
	dist = [float('inf')] * card_V  # dist[i] holds the distance from the source vertex to vertex i
	pi = [None] * card_V
	color[source] = GRAY
	dist[source] = 0

	q = Queue(card_V)
	q.enqueue(source)
	while not q.is_empty():
		u = q.dequeue()
		for edge in G.get_adj_list(u):  # search the neighbors of u
			v = edge.get_v()
			if color[v] == WHITE:  # is v being discovered now?
				color[v] = GRAY 
				dist[v] = dist[u] + 1 	# add 1 to distance for v
				pi[v] = u 	# assign predecessor
				q.enqueue(v)  # v is now on the frontier
		color[u] = BLACK  # u is now behind the frontier
	return dist, pi


# Testing
if __name__ == "__main__":

	import numpy as np
	from generate_random_graph import generate_random_graph

	# Directed.
	card_V = 10
	graph1 = generate_random_graph(card_V, 0.25, True)
	print(graph1)
	s = 5
	dist, predecessor = bfs(graph1, s)
	for i in range(card_V):
		print(str(i) + ": dist = " + str(dist[i]) + ", path = " +
				str(print_path(predecessor, s, i, lambda i: i)))
	print()

	# Undirected, textbook example.
	vertices = ['r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	edges = [('r', 's'), ('r', 't'), ('r', 'w'), ('s', 'u'), ('s', 'v'),
			 ('t', 'u'), ('u', 'y'), ('v', 'w'), ('v', 'y'), ('w', 'x'),
			 ('w', 'z'), ('x', 'y'), ('x', 'z')]
	card_V = len(vertices)
	graph2 = AdjacencyListGraph(card_V, False)
	for edge in edges:
		graph2.insert_edge(vertices.index(edge[0]), vertices.index(edge[1]))
	print(graph2.strmap(lambda i: vertices[i]))
	s = vertices.index('s')
	dist, predecessor = bfs(graph2, s)  # BFS from s
	for i in range(card_V):
		print(vertices[i] + ": dist = " + str(dist[i]) + ", path = " + \
				str(print_path(predecessor, s, i, lambda i: vertices[i])))
