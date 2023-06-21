#!/usr/bin/env python3
# ford_fulkerson.py

# Introduction to Algorithms, Fourth edition
# Linda Xiao

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


def dfs(G, source, sink):
	"""Perform depth-first search on a residual network in order to find an augmenting path
	from the source to the sink.  Stops as soon as the sink is found.  Doesn't
	run any functions upon discovering or finishing a vertex.

	Arguments:
	G -- a residual network
	s -- index of source
	t -- index of sink

	Returns:
	pi -- if vertex v is found in the search, then pi[v] is the edge (u, v) that was explored to find v.
	"""

	global pi, sink_found
	sink_found = False
	pi = [None] * G.get_card_V()

	# Find a path from the source to the sink, if one exists.
	dfs_visit(G, source, sink)
	return pi


def dfs_visit(G, u, sink):
	"""Perform depth-first search on a residual network in order to find an augmenting path
	from the source to the sink.  Stops as soon as the sink is found.  Doesn't
	run any functions upon discovering or finishing a vertex.

	Arguments:
	G -- a residual network
	u -- index of the vertex currently searching from
	sink -- index of sink
	"""
	global pi, sink_found

	if sink_found:
		return  # a previous call of this function found the sink

	# Explore each adjacent edge, but only if the sink has not yet been found.
	for edge in G.get_adj_list(u):
		if sink_found:
			return
		v = edge.get_v()
		# Explore this edge (u, v) if v has not been discovered (pi[v] is None)
		# and the edge has positive capacity (it's in the residual network).
		if pi[v] is None and edge.c > 0:
			pi[v] = edge
			if v == sink:
				sink_found = True  # no need to search any further
			else:
				dfs_visit(G, v, sink)


def ford_fulkerson(G, source, sink, search_func=dfs):
	"""Find a maximum flow in a flow network from source to sink.

	Arguments:
	G -- a flow network with no antiparallel edges
	source -- index of source vertex
	sink -- index of sink vertex
	search_func -- search func to determine whether a path exists from source to sink;
	defaults to dfs

	Returns:
	max_flow -- value of the maximum flow found
	The c instance variables of the edges contain the flow values for the maximum flow
	"""
	residual_network = G.create_residual_network()  # edge flows already initialized to 0
	max_flow = 0

	# Try to find an augmenting path in the residual network.
	pi = search_func(residual_network, source, sink)

	# Iterate as long as there is an augmenting path from source to sink in the residual network.
	# If pi[sink] is None, then sink is unreachable from source in the residual network.
	while pi[sink] is not None:
		# Find the minimum residual capacity of the augmenting path.
		residual_capacity = float('inf')
		v = sink
		while v != source:
			residual_capacity = min(residual_capacity, pi[v].get_capacity())
			v = pi[v].get_u()
		max_flow += residual_capacity

		# Update the flow for each edge on the augmenting path. When updating the flow,
		# update the residual network.
		v = sink
		while v != source:
			edge = pi[v]  # edge is on the augmenting path
			if edge.original_edge.get_u() == edge.get_u():  # edge exists in the original flow network
				edge.original_edge.f += residual_capacity   # add the residual capacity
				residual_network.update_residual_edge(edge)
			else:  # edge does not exist in the original flow network
				edge.original_edge.f -= residual_capacity 	# subtract the residual capacity
				residual_network.update_residual_edge(edge)
			v = edge.get_u()  # go to the previous edge in the augmenting path

		# Try to find an augmenting path in the new residual network.
		pi = search_func(residual_network, source, sink)

	return max_flow


def bfs(G, source, sink):
	"""Perform breadth-first search on a residual network in order to find an augmenting path
	from the source to the sink.  Stops as soon as the sink is found.

	Arguments:
	G -- a residual network
	s -- index of source
	t -- index of sink

	Returns:
	pi -- if vertex v is found in the search, then pi[v] is the edge (u, v) that was explored to find v.
	"""

	card_V = G.get_card_V()
	pi = [None] * card_V

	q = Queue(card_V)
	q.enqueue(source)
	# Search ls long as there are undiscovered vertices.  If the sink is discovered,
	# return from within the while loop.
	while not q.is_empty():
		u = q.dequeue()
		# Explore each edge leaving u.
		for edge in G.get_adj_list(u):
			v = edge.get_v()
			# Explore this edge (u, v) if v has not been discovered (pi[v] is None)
			# and the edge has positive capacity (it's in the residual network).
			if pi[v] is None and edge.c > 0:
				pi[v] = edge
				if v == sink:  # discovered the sink?
					return pi
				q.enqueue(v)

	return pi


def edmonds_karp(G, source, sink):
	"""The Edmonds-Karp algorithm for maximum flow.  Ford-Fulkerson, but with augmenting paths
	found by breadth-first search.

	Arguments:
	G -- a flow network with no antiparallel edges
	source -- index of source vertex
	sink -- index of sink vertex

	Returns:
	max_flow -- value of the maximum flow found
	The c instance variables of the edges contain the flow values for the maximum flow
	"""
	# Edmonds-Karp implements Ford-Fulkerson with BFS.
	return ford_fulkerson(G, source, sink, bfs)


# Testing
if __name__ == "__main__":

	from flow_network import FlowNetwork
	import numpy as np

	# Example from textbook with 6 vertices.
	n = 6
	graph1 = FlowNetwork(6)
	graph1.insert_edge(0, 1, 16)
	graph1.insert_edge(0, 2, 13)
	graph1.insert_edge(1, 3, 12)
	graph1.insert_edge(2, 1, 4)
	graph1.insert_edge(2, 4, 14)
	graph1.insert_edge(3, 2, 9)
	graph1.insert_edge(3, 5, 20)
	graph1.insert_edge(4, 3, 7)
	graph1.insert_edge(4, 5, 4)
	print(graph1)
	graph2 = graph1.copy()
	# Ford-Fulkerson with augmenting path found by depth-first search.
	# Source is vertex 0, sink is vertex 5.
	print("Ford-Fulkerson")
	max_flow = ford_fulkerson(graph1, 0, 5)
	print(max_flow)
	print(graph1)

	# Edmonds-Karp implementation.
	print("Edmonds-Karp")
	max_flow = edmonds_karp(graph2, 0, 5)
	print(max_flow)
	print(graph2)

	# Large example.
	graph3 = FlowNetwork(50)
	for i in range(50):
		for j in range(np.random.randint(10)):
			rand = np.random.randint(i, 50)
			if rand != i:
				try:
					# Ignore multiple edge inserts, keep first one.
					graph3.insert_edge(i, rand, np.random.randint(50))
				except RuntimeError:
					pass
	print(graph3)
	graph4 = graph3.copy()

	# Should be the same.
	print("Ford-Fulkerson")
	ff_max_flow = ford_fulkerson(graph3, 13, 37)
	print(ff_max_flow)
	print(graph3)
	print("Edmonds-Karp")
	ek_max_flow = edmonds_karp(graph4, 13, 37)
	print(ek_max_flow)
	print(graph4)
	print("Max flow values of " + str(ff_max_flow) + " and " + str(ek_max_flow) + " are "
		  + ["not ", ""][ff_max_flow == ek_max_flow] + "equal")
