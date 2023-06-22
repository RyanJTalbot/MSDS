#!/usr/bin/env python3
# topological_sort.py

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

from dll_sentinel import DLLSentinel
from dfs import dfs


def finish(u):
	"""Prepend onto the linked list as each vertex is finished."""
	global ordered_list
	ordered_list.prepend(u)


def topological_sort(G):
	"""Topologically sort a directed acyclic graph.

	Input:
	G -- a dag, represented by adjacency lists.

	Returns:
	A linked list giving the topologically sorted order of the vertices.
	"""
	global ordered_list
	if not G.is_directed():
		raise RuntimeError("Graph must be directed.")
	ordered_list = DLLSentinel()
	dfs(G, None, None, finish)  # no start_dfs_tree or discovery_func
	return ordered_list


# Testing
if __name__ == "__main__":

	import numpy as np 
	from adjacency_list_graph import AdjacencyListGraph

	# Directed graph.
	array1 = np.arange(10)
	graph1 = AdjacencyListGraph(10)
	for i in range(0, len(array1) - 1):
		graph1.insert_edge(array1[i], array1[i + 1])
	print(graph1)
	print(topological_sort(graph1))
	print()

	# Textbook example.
	clothing = ["shirt", "tie", "jacket", "belt", "watch", "undershorts", "pants", "socks", "shoes"]
	graph2 = AdjacencyListGraph(len(clothing))
	dependencies = [("undershorts", "pants"), ("undershorts", "shoes"), ("socks", "shoes"),
					("pants", "shoes"), ("pants", "belt"), ("shirt", "tie"), ("shirt", "belt"),
					("belt", "jacket"), ("tie", "jacket")]
	for dependency in dependencies:
		graph2.insert_edge(clothing.index(dependency[0]), clothing.index(dependency[1]))
	print(graph2.strmap(lambda i: clothing[i]))
	clothing_order = topological_sort(graph2)
	for data in clothing_order.iterator():
		print(clothing[data])
	print()

	# Undirected. 
	graph3 = AdjacencyListGraph(10, False)
	graph3.insert_edge(1, 2)
	graph3.insert_edge(4, 7)
	try: 
		topological_sort(graph3)
	except RuntimeError as e:
		print(e)
