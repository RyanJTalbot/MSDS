#!/usr/bin/env python3
# hopcroft_karp.py

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

from adjacency_list_graph import Edge, AdjacencyListGraph
from fifo_queue import Queue


def make_G_M(G, left, M):
    """Creates the directed version G_M of the undirected bipartite graph G.

    Arguments:
        G -- the undirected bipartite graph, represented by adjacency lists
        left -- the set L of vertices in G
        M -- the current matching, represented as a set of edges in G of the form (l, r),
        where l is in L and r is in R

    Returns:
        The graph G_M
        """

    G_M = AdjacencyListGraph(G.get_card_V())
    for l in left:
        for edge in G.get_adj_list(l):
            r = edge.get_v()
            if edge in M:
                G_M.insert_edge(r, l)  # edges in M go right to left in G_M
            else:
                G_M.insert_edge(l, r)  # edges not in M go left to right in G_M

    return G_M


def make_H_T(G_M, left, matched):
    """Makes the directed acyclic graph H^T by performing breadth-first search from all
    unmatched vertices in L up to and including the distance to the first unmatched
    vertex in R.

    Arguments:
        G_M -- the directed graph created by make_G_M
        left -- the set L of vertices in G
        matched -- matched[u] is True is vertex u is matched under the current matching,
        False if not matched

    Returns:
        The dag H^T (the transpose of H).
        The breadth-first distances of vertices in H.
        q -- the maximum breadth-first distance of an unmatched vertex in R within H.
    """
    card_V = G_M.get_card_V()
    dist = [float('inf')] * card_V
    queue = Queue(card_V)

    # Start the BFS with all unmatched vertices in L in the queue.
    for l in left:
        if not matched[l]:
            queue.enqueue(l)
            dist[l] = 0

    # Perform BFS until encountering the first vertex with a distance greater
    # than the distance to the first unmatched vertex in R.
    q = float('inf')
    while not queue.is_empty():
        u = queue.dequeue()
        if dist[u] >= q:
            break  # any vertices newly discovered from u have distance > q
        for edge in G_M.get_adj_list(u):  # search the neighbors of u
            v = edge.get_v()
            if dist[v] == float('inf'):  # is v being discovered now?
                dist[v] = dist[u] + 1 	# add 1 to distance for v
                queue.enqueue(v)  # v is now on the frontier

                # If v is in R and unmatched, then v's distance becomes q.
                # Because G_M is bipartite, v is in R if and only if v's distance is odd.
                if dist[v] % 2 == 1 and not matched[v] and q == float('inf'):
                    q = dist[v]

    # The dag H consists of all vertices with distances <= q.
    # To avoid renumbering edges, use the same vertices in H as in G_M, but
    # include only edges leaving vertices with distances < q.
    # Edges in H go from vertices at distance d to vertices at distance d+1.
    # Instead of constructing H, we need its transpose, so construct H^T.
    H_T = AdjacencyListGraph(card_V)
    for u in range(card_V):
        if dist[u] < q:
            for edge in G_M.get_adj_list(u):
                v = edge.get_v()
                if dist[v] == dist[u] + 1:
                    H_T.insert_edge(v, u)  # insert the reverse of the edge in G_M

    return H_T, dist, q


def find_maximal_vertex_disjoint_augmenting_paths(H_T, right, dist, q, matched):
    """Find a maximal set of vertex-disjoint shortest M-augmenting paths in H^T.
    Perform a depth-first search from each unmatched vertex in R, until
    discovering a vertex with breadth-first distance 0 in H (which must be an
    unmatched vertex in L) or exhausting all possible paths.)

    Arguments:
        H_T -- transpose of the dag H
        right -- the set R of vertices
        dist -- breadth-first distances in H from unmatched vertices in L
        q -- maximum breadth-first distance in H
        matched -- matched[u] is True is vertex u is matched under the current matching,
        False if not matched

    Returns:
        pi -- pi[u] is the predecessor vertex of u in the DFS.
        """

    pi = [None] * H_T.get_card_V()
    for r in right:
        # Start a depth-first search from each unmatched vertex in R at distance q.
        if dist[r] == q and not matched[r]:
            dfs(H_T, r, dist, pi)

    return pi


def dfs(H_T, u, dist, pi):
    """Perform depth-first search in H_T starting from vertex u, but stopping if a vertex with
    dist = 0 is discovered.

    Arguments:
        H_T -- transpose of the dag H
        u -- vertex to search from
        dist -- breadth-first distances in H from unmatched vertices in L
        pi -- pi[u] is the predecessor vertex of u in the DFS.

    Returns:
        True if the search found a vertex with dist = 0.
        Also updates pi values.
        """

    # Search each edge leaving u, but stopping if a vertex with dist = 0 is discovered.
    for edge in H_T.get_adj_list(u):
        v = edge.get_v()
        if pi[v] is None:  # is v newly discovered?
            pi[v] = u
            if dist[v] == 0:
                return True  # discovered a vertex with dist = 0
            else:
                if dfs(H_T, v, dist, pi):
                    return True  # the search from v discovered a vertex with dist = 0
    return False  # the search from u did not discover a vertex with dist = 0


def hopcroft_karp(G, left, right):
    """The Hopcroft-Karp algorithm to find a maximum matching in an undirected bipartite graph.
    Repeatedly finds a maximal set of vertex-disjoint shortest augmenting paths and adds their
    symmetric difference into the matching found so far.  Stops when there are no more
    augmenting paths.

    Arguments:
        G -- the undirected bipartite graph, represented by adjacency lists
        left, right -- the sets L and R of vertices of G

    Returns:
        The maximum matching M, represented as a set of edges in G of the form (l, r),
        where l is in L and r is in R
        """
    M = set()  # M starts out as an empty set
    card_V = G.get_card_V()
    matched = [False] * card_V  # no vertices matched yet

    while True:
        G_M = make_G_M(G, left, M)  # make the directed graph G_M
        H_T, dist, q = make_H_T(G_M, left, matched)  # make the transpose H^T of the dag H

        # Perform DFS from each unmatched vertex in R in H^T to find augmenting paths to
        # unmatched vertices in L.  pi contains the results of the depth-first searches.
        pi = find_maximal_vertex_disjoint_augmenting_paths(H_T, right, dist, q, matched)

        found_augmenting_path = False  # stop when no augmenting paths found

        # For each unmatched vertex in L, try to trace back a path to an unmatched vertex in R.
        for l in left:
            if not matched[l] and pi[l] is not None:  # if pi[l] is None, no path to l was found
                path = set()  # trace the augmenting path, edge by edge
                u = l  # start at the unmatched vertex in L
                while pi[u] is not None:
                    # Add edges into the path, always of the form (l, r) with l in L and r in R.
                    if u in left:
                        path.add(G.find_edge(u, pi[u]))
                    else:
                        path.add(G.find_edge(pi[u], u))
                    u = pi[u]  # go to the previous vertex in the augmenting path

                matched[l] = True  # the augmenting path ends at l
                matched[u] = True  # and it starts at u
                found_augmenting_path = True  # don't stop yet
                M ^= path  # take the symmetric difference of current matching and this path

        if not found_augmenting_path:  # all done?
            return M


# Testing
if __name__ == "__main__":
    from maximum_bipartite_matching import *
    from random import randint, sample

    # Example from textbook with the graph in Figure 25.1.
    vertices = ['l_1', 'l_2', 'l_3', 'l_4', 'l_5', 'l_6', 'l_7',
                'r_1', 'r_2', 'r_3', 'r_4', 'r_5', 'r_6', 'r_7', 'r_8']
    edges = [('l_1', 'r_2'), ('l_1', 'r_3'), ('l_2', 'r_1'), ('l_2', 'r_2'), ('l_3', 'r_1'),
             ('l_3', 'r_3'), ('l_3', 'r_4'), ('l_3', 'r_5'), ('l_3', 'r_6'), ('l_4', 'r_2'),
             ('l_4', 'r_3'), ('l_4', 'r_7'), ('l_5', 'r_4'), ('l_5', 'r_5'), ('l_5', 'r_6'),
             ('l_5', 'r_7'), ('l_6', 'r_3'), ('l_6', 'r_7'), ('l_7', 'r_5'), ('l_7', 'r_8')]
    graph1 = AdjacencyListGraph(len(vertices), False)
    for edge in edges:
        graph1.insert_edge(vertices.index(edge[0]), vertices.index(edge[1]))
    print(graph1.strmap(lambda i: vertices[i]))
    left = {*[vertices.index(l) for l in ['l_1', 'l_2', 'l_3', 'l_4', 'l_5', 'l_6', 'l_7']]}
    right = {*[vertices.index(r) for r in ['r_1', 'r_2', 'r_3', 'r_4', 'r_5', 'r_6', 'r_7', 'r_8']]}

    ## Uncomment these lines to test make_G_M, make_H_T, and find_maximal_vertex_disjoint_augmenting_paths
    ## with the example in Figures 25.2 and 25.3.
    # matching = {graph1.find_edge(vertices.index('l_2'), vertices.index('r_2')),
    #             graph1.find_edge(vertices.index('l_3'), vertices.index('r_3')),
    #             graph1.find_edge(vertices.index('l_7'), vertices.index('r_5')),
    #             graph1.find_edge(vertices.index('l_5'), vertices.index('r_7'))}
    # matched = [False, True, True, False, True, False, True, False, True, True, False, True, False, True, False]
    #
    # G_M = make_G_M(graph1, left, matching)
    # print(G_M.strmap(lambda i: vertices[i]))
    # H_T, dist, q = make_H_T(G_M, left, matched)
    # # The next 4 lines cause DFS to make the same choices as in Figure 25.3
    # H_T.delete_edge(vertices.index('r_1'), vertices.index('l_2'))
    # H_T.insert_edge(vertices.index('r_1'), vertices.index('l_2'))
    # H_T.delete_edge(vertices.index('r_7'), vertices.index('l_4'))
    # H_T.insert_edge(vertices.index('r_7'), vertices.index('l_4'))
    # print(dist, q)
    # print(H_T.strmap(lambda i: vertices[i]))
    # pi = find_maximal_vertex_disjoint_augmenting_paths(H_T, right, dist, q, matched)
    # for i in range(len(vertices)):
    #     if pi[i] is not None:
    #         print(vertices[i], vertices[pi[i]])

    # Find a maximum matching for the example in Figure 25.1.
    matching = hopcroft_karp(graph1, left, right)
    print_edges(graph1, matching, lambda i: vertices[i])
    print(is_matching(graph1, matching))
    print()

    # Try on a random bipartite graph.
    card_l = 30
    card_r = 40
    left = list(range(card_l))
    right = [card_l + i for i in range(card_r)]
    num_vertices = card_l + card_r
    graph2 = AdjacencyListGraph(num_vertices, False)

    for l in left:
        degree = randint(1, 4)
        neighbors = sample(right, degree)
        for r in neighbors:
            graph2.insert_edge(l, r)

    print(graph2)
    flow_matching = maximum_bipartite_matching(graph2, left, right)
    hk_matching = hopcroft_karp(graph2, left, right)
    print("Flow matching")
    print_edges(graph2, flow_matching)
    print(is_matching(graph2, flow_matching))
    print("HK matching")
    print_edges(graph2, hk_matching)
    print(is_matching(graph2, hk_matching))
    print(len(flow_matching), len(hk_matching))
    if not is_matching(graph2, flow_matching) or \
            not is_matching(graph2, hk_matching) or len(flow_matching) != len(hk_matching):
        print("Error")
