#!/usr/bin/env python3
# hungarian.py

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

import numpy as np
from fifo_queue import Queue
from itertools import permutations


def default_vertex_labeling(W, n):
    """Return the default vertex labeling for a bipartite graph.

    Arguments:
        W -- the weight matrix
        n -- number of vertices in L and in R; W is n x n

    Returns:
        h_l -- labels for vertices in L
        h_r -- labels for vertices in R
        """
    # For h_l, find the maximum value in each row.  All h_r values are 0.
    return np.amax(W, axis=1), [0] * n


def greedy_bipartite_matching(W, h_l, h_r, n):
    """Create a bipartite matching by the greedy method.

    Arguments:
        W -- the weight matrix
        h_l -- labels for vertices in L
        h_r -- labels for vertices in R
        n -- number of vertices in L and in R; W is n x n

    Returns:
        A set of edges in the greedy matching.
        """

    M = set()  # the greedy matching
    matched = [False] * n  # matched[r] for r in R if r is matched, False if not

    for l in range(n):
        for r in range(n):
            if h_l[l] + h_r[r] == W[l,r] and not matched[r]:
                M.add((l, r))  # greedily add edge (l, r) to the matching
                matched[r] = True
                break

    return M


def find_augmenting_path(W, h_l, h_r, matched_l, matched_r, M, n):
    """
    Find some M-augmenting path in G_M,h, updating the h labels h_l and h_r if necessary.

    Arguments:
        W -- the weight matrix
        h_l -- labels for vertices in L
        h_r -- labels for vertices in R
        matched_l -- matched_l for l in L is True if l is matched, False if not
        matched_r -- matched_r for r in R is r's matched vertex in L if r is matched, None if not
        M -- the matching so far
        n -- number of vertices in L and in R; w is n x n

    Returns:
        An augmenting path as a set of edges (l, r), where l in L and r in R.
    """
    queue = Queue(2*n)  # queue contains tuples of vertex number and True/False: True if in R, False if in L
    f_l = set()  # F_L comprises vertices in L in the depth-first forest so far
    f_r = set()  # F_R comprises vertices in R in the depth-first forest so far
    pi_l = [None] * n  # breadth-first predecessors for vertices in L
    pi_r = [None] * n  # breadth-first predecessors for vertices in R
    vertices = set(range(n))

    for l in vertices:
        if not matched_l[l]:
            queue.enqueue((l, False))  # queue starts with all unmatched vertices in L
            f_l.add(l)  # as does F_L

    found_augmenting_path = False

    while not found_augmenting_path:
        if queue.is_empty():  # ran out of vertices to search from?
            old_h_l = list(h_l)
            old_h_r = list(h_r)
            delta = min([h_l[l] + h_r[r] - W[l,r] for l in f_l for r in vertices - f_r])
            for l in f_l:
                h_l[l] -= delta
            for r in f_r:
                h_r[r] += delta

            # Find the new edges in G_M,h.
            for l in vertices:
                if found_augmenting_path:
                    break
                for r in vertices:
                    # (l, r) is a new edge in G_M,h if the changes in h_l and h_r make
                    # h_l[l] + h_r[r] == W[l,r] when h_l[l] + h_r[r] > W[l,r] before h_l and h_r
                    # changed, and also if (l, r) is not in M (because then (r, l) would be in G_M,h).
                    if r not in f_r and old_h_l[l] + old_h_r[r] > W[l,r] and h_l[l] + h_r[r] == W[l,r] \
                            and (l, r) not in M:
                        # r is not in F_R and (l, r) is a new edge in G_M,h.
                        # Discover r and add it to the breadth-first forest.
                        pi_r[r] = l
                        if matched_r[r] is None:
                            # Found an augmenting path.
                            found_augmenting_path = True
                            break
                        else:
                            queue.enqueue((r, True))
                            f_r.add(r)

            if found_augmenting_path:
                break

        # At this point, the queue is not empty.
        u, side = queue.dequeue()
        if side:
            # u is in R and matched.  Its neighbor l in G_M,h is in matched_r[u].
            l = matched_r[u]
            # (u, l) is the only edge leaving u in G_M,h.
            # Discover l and add it to F_L.
            pi_l[l] = u
            f_l.add(l)
            queue.enqueue((l, False))
        else:
            # u is in L.  Find each neighbor in R that is not in F_R.
            for r in vertices:
                if r not in f_r and h_l[u] + h_r[r] == W[u,r] and (u, r) not in M:
                    pi_r[r] = u
                    if matched_r[r] is None:
                        # Found an augmenting path.
                        found_augmenting_path = True
                        break
                    else:
                        queue.enqueue((r, True))
                        f_r.add(r)

    # The last vertex discovered in R ends an augmenting path.  Trace it back.
    l = pi_r[r]
    path = {(l, r)}
    matched_r[r] = l  # because this edge (l, r) will be added to the matching
    while pi_l[l] is not None:
        r = pi_l[l]
        path.add((l, r))  # this edge (l, r) will be removed from the matching
        l = pi_r[r]
        path.add((l, r))
        matched_r[r] = l  # because this edge (l, r) will be added to the matching
    matched_l[l] = True

    return path


def hungarian(W, n):
    """
    Finds a maximum-weight perfect matching for a weighted bipartite graph with n vertices
    in L and n vertices in R.  Uses the Hungarian algorithm, but without the optimization
    in Problem 25-2.

    Arguments:
        W -- the weight matrix
        n -- number of vertices in L and in R; w is n x n

    Returns:
        A maximum-weight perfect matching as a set of edges (l, r), where l in L and r in R.
    """
    h_l, h_r = default_vertex_labeling(W, n)  # initial vertex labels
    M = greedy_bipartite_matching(W, h_l, h_r, n)  # initial matching
    matched_l = [False] * n  # matched_l[l] for l in L is True iff l is matched
    matched_r = [None] * n  # matched_r[r] for r in R is r's matching vertex in L, or None if r is unmatched
    for (l, r) in M:
        matched_l[l] = True
        matched_r[r] = l

    while len(M) < n:  # matching has n edges once it becomes a perfect matching
        p = find_augmenting_path(W, h_l, h_r, matched_l, matched_r, M, n)
        M ^= p  # take the symmetric difference of current matching and this path

    return M


def total_weight(W, edges):
    """Return the sum of edge weights for a set of edges."""
    return sum([W[l,r] for (l, r) in edges])


def brute_force(W, n):
    """
    Finds a maximum-weight perfect matching for a weighted bipartite graph with n vertices
    in L and n vertices in R.  Uses brute force by trying all n! possibilities.

    Arguments:
        W -- the weight matrix
        n -- number of vertices in L and in R; w is n x n

    Returns:
        A maximum-weight perfect matching as a set of edges (l, r), where l in L and r in R.
    """
    best_cost = float('-inf')
    best_matching = None
    for perm in permutations(range(n)):  # try every permutation of vertices in R
        matching = [(l, perm[l]) for l in range(n)]
        cost = total_weight(W, matching)

        if cost > best_cost:  # do we have a new winner?
            best_cost = cost
            best_matching = matching

    return best_matching


# Testing
if __name__ == "__main__":
    # Example from textbook, with vertices in L and R indexed 0 to n-1.
    n = 7
    W = np.array([[4, 10, 10, 10, 2, 9, 3],
                  [6, 8, 5, 12, 9, 7, 2],
                  [11, 9, 6, 7, 9, 5, 15],
                  [3, 9, 6, 7, 5, 6, 3],
                  [2, 6, 5, 3, 2, 4, 2],
                  [10, 8, 11, 4, 11, 2, 11],
                  [3, 4, 5, 4, 3, 6, 8]])

    hungarian_solution = hungarian(W, n)
    print("Matching:", hungarian_solution)

    # Find the total weight of the matching.
    hungarian_weight = total_weight(W, hungarian_solution)
    print("Weight:", hungarian_weight)

    # Check against the brute-force solution.
    brute_force_solution = brute_force(W, n)
    brute_force_weight = total_weight(W, brute_force_solution)
    if hungarian_weight != brute_force_weight:
        print("Does not match brute force weight of", brute_force_weight)
