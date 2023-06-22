#!/usr/bin/env python3
# generate_random_graph.py

# Introduction to Algorithms, Fourth edition
# Tom Cormen

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

from random import randint, random
from adjacency_list_graph import AdjacencyListGraph
from adjacency_matrix_graph import AdjacencyMatrixGraph


def generate_random_graph(card_V, edge_probability, by_adjacency_lists=True,
                          directed=True, weighted=False, min_weight=0, max_weight=20):
    """Generate and return a random graph.

    Arguments:
        card_V -- number of vertices
        edge_probability -- probability that a given edge is present
        by_adjacency_lists -- True if the graph is represented by adjacency lists,
        False if by an adjacency matrix
        directed -- True if the graph is directed, False if undirected
        weighted -- True if the graph is weighted, False if unweighted
        min_weight -- if weighted, the minimum weight of an edge
        max_weight -- if weighted, the maximum weight of an edge

    Returns:
        A graph
        """
    constructor = AdjacencyListGraph if by_adjacency_lists else AdjacencyMatrixGraph
    G = constructor(card_V, directed, weighted)

    for u in range(card_V):
        if directed:
            min_v = 0
        else:
            min_v = u + 1

        for v in range(min_v, card_V):
            if random() <= edge_probability:  # add edge (u, v)
                if weighted:
                    weight = randint(min_weight, max_weight)  # random weight within range
                else:
                    weight = None
                G.insert_edge(u, v, weight)  # guaranteed that edge (u, v) is not already present

    return G


# Testing
if __name__ == "__main__":
    graph1 = generate_random_graph(20, 0.12)
    print(graph1)

    graph2 = generate_random_graph(10, 0.15, False, False, False)
    print(graph2)
    print()

    graph3 = generate_random_graph(18, 0.25, False, False, True, 3, 7)
    print(graph3)
