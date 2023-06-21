#!/usr/bin/env python3
# mst.py

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

from merge_sort import merge_sort
from adjacency_list_graph import AdjacencyListGraph
from disjoint_set_forest import make_set, find_set, union
from min_heap_priority_queue import MinHeapPriorityQueue


class KruskalEdge:

    def __init__(self, u, v, weight=None):
        """Initialize edge class that contains both endpoints and weight."""
        self.u = u
        self.v = v
        if weight is not None:
            self.weight = weight

    def get_u(self):
        """Return endpoint of vertex that edge starts."""
        return self.u

    def get_v(self):
        """Return endpoint of vertex that edge ends."""
        return self.v

    def get_weight(self):
        """Return weight of edge."""
        return self.weight

    def __le__(self, edge2):
        """Compare weights for less than or equal to."""
        return self.weight <= edge2.weight

    def __str__(self):
        """Print edge with endpoints and weight."""
        return "(" + str(self.u) + ", " + str(self.v) + "), weight: " + str(self.weight)


def kruskal(G):
    """ Return the minimum spanning tree of a weighted, undirected graph G using Kruskal's algorithm."""
    if G.is_directed():
        raise RuntimeError("Graph should be undirected.")

    card_V = G.get_card_V()
    # Initialize an undirected, weighted, minimum spanning tree.
    mst = AdjacencyListGraph(card_V, False, True)
    # Keep an array of handles to disjoint-set objects.
    forest = [None] * card_V
    for v in range(card_V):
        forest[v] = make_set(v)

    # Make an array of weighted edges and sort it by weight.
    edges = []

    for u in range(card_V):
        for edge in G.get_adj_list(u):
            if u < edge.v:  # append edge only once
                edges.append(KruskalEdge(u, edge.get_v(), edge.get_weight()))
    merge_sort(edges)  # sort in nondecreasing order by weight

    # Examine each edge.
    for edge in edges:
        u = forest[edge.get_u()]
        v = forest[edge.get_v()]
        # If the endpoints are not in the same tree, connect the trees.
        if find_set(u) != find_set(v):
            mst.insert_edge(edge.get_u(), edge.get_v(), edge.get_weight())
            union(u, v)

    return mst


def prim(G, r):
    """ Return the minimum spanning tree of a weighted, undirected graph G using Prim's algorithm.

    Arguments:
    G -- an undirected graph, represented by adjacency lists
    r -- root vertex to start from
    """
    # Initialize keys and predecessors.
    card_V = G.get_card_V()
    pi = [None] * card_V
    visited = [False] * card_V  # visited vertices are in the MST
    key = [float('inf')] * card_V  # vertices not yet in MST
    key[r] = 0  # root r has key 0

    # Initialize the min-priority queue of vertices.
    queue = MinHeapPriorityQueue(lambda u: key[u])
    for u in range(card_V):
        queue.insert(u)

    while queue.get_size() > 0:
        u = queue.extract_min()  # add u to the tree
        visited[u] = True
        for edge in G.get_adj_list(u):  # update the keys of u's non-tree neighbors
            v = edge.get_v()
            weight = edge.get_weight()
            if not visited[v] and weight < key[v]:  # update v's key?
                pi[v] = u
                key[v] = weight
                queue.decrease_key(v, weight) 	# update v in the min-priority queue

    # Make the MST as an undirected, weighted graph.
    mst = AdjacencyListGraph(card_V, False, True)
    for i in range(card_V):
        # Insert edges from vertices and their predecessors.
        if pi[i] is not None:
            mst.insert_edge(pi[i], i, key[i])

    return mst


def get_total_weight(G):
    """Return the total weight of edges in an undirected graph G."""
    total_weight = 0
    for u in range(G.get_card_V()):
        for edge in G.get_adj_list(u):
            v = edge.get_v()
            if u < v:
                total_weight += edge.get_weight()
    return total_weight


def print_undirected_edges(G, vertices):
    """Print the edges in an undirected graph G."""
    for u in range(G.get_card_V()):
        for edge in G.get_adj_list(u):
            v = edge.get_v()
            if u < v:
                print("(" + str(vertices[u]) + ", " + str(vertices[v]) + ")")


# Testing
if __name__ == "__main__":

    import numpy as np
    from generate_random_graph import generate_random_graph

    # Example from book.
    vertices = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    edges = [('a', 'b', 4), ('a', 'h', 8), ('b', 'c', 8), ('b', 'h', 11), ('c', 'd', 7),
             ('c', 'f', 4), ('c', 'i', 2), ('d', 'e', 9), ('d', 'f', 14), ('e', 'f', 10),
             ('f', 'g', 2), ('g', 'h', 1), ('g', 'i', 6), ('h', 'i', 7)]
    graph1 = AdjacencyListGraph(len(vertices), False, True)
    for edge in edges:
        graph1.insert_edge(vertices.index(edge[0]), vertices.index(edge[1]), edge[2])
    print(graph1.strmap(lambda i: vertices[i]))
    print("MST with Kruskal's algorithm:")
    kruskal1 = kruskal(graph1)
    print_undirected_edges(kruskal1, vertices)
    kruskal_weight = get_total_weight(kruskal1)
    print("Kruskal weight =", kruskal_weight)
    print("MST with Prim's algorithm:")
    prim1 = prim(graph1, 0)
    print_undirected_edges(prim1, vertices)
    prim_weight = get_total_weight(prim1)
    print("Prim weight =", prim_weight)
    print(prim_weight == kruskal_weight)
    print()

    # Larger example.
    card_V = 50
    vertices = list(range(card_V))
    graph2 = generate_random_graph(card_V, 0.15, True, False, True, 2, 15)
    print(graph2)
    print("MST with Kruskal's algorithm:")
    kruskal2 = kruskal(graph2)
    print_undirected_edges(kruskal2, vertices)
    kruskal_weight2 = get_total_weight(kruskal2)
    print("Kruskal weight =", kruskal_weight2)
    print("MST with Prim's algorithm:")
    prim2 = prim(graph2, 0)
    print_undirected_edges(prim2, vertices)
    prim_weight2 = get_total_weight(prim2)
    print("Prim weight =", prim_weight2)
    print(prim_weight2 == kruskal_weight2)
