#!/usr/bin/env python3
# difference_constraints.py

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

from adjacency_list_graph import *
from bellman_ford import bellman_ford


def difference_constraints(constraints):
    """Solve a system of difference constraints.

    Input:
    constraints -- a list (or tuple) of lists (or tuples) of three values: i, j, w,
    indicating the constraint xi - xj <= w, where i, j >= 1.

    Returns:
    feasible -- boolean indicating whether the system has a feasible solution
    solution -- a list of solution values for the xi
    """

    # Determine the highest variable index.
    n = 0
    for constraint in constraints:
        n = max(n, constraint[0], constraint[1])

    # Create the constraint graph.
    constraint_graph = AdjacencyListGraph(n+1, True, True)
    for constraint in constraints:
        # Add edge (vi, vj) for constraint xj - xi.
        constraint_graph.insert_edge(constraint[1], constraint[0], constraint[2])
    # Add the edges from v0.
    for i in range(1, n+1):
        constraint_graph.insert_edge(0, i, 0)

    # If no negative-weight cycle, then shortest-path weights from v0 are a solution.
    d, pi, feasible = bellman_ford(constraint_graph, 0)
    return feasible, d[1:]


# Testing
if __name__ == "__main__":
    # Example from textbook.
    constraints1 = [(1, 2, 0), (1, 5, -1), (2, 5, 1), (3, 1, 5),
                   (4, 1, 4), (4, 3, -1), (5, 3, -3), (5, 4, -3)]
    print(difference_constraints(constraints1))

    # Add a negative-weight cycle.
    constraints2 = [(1, 2, 0), (1, 5, -1), (2, 5, 1), (3, 1, 4),
                    (4, 1, 4), (4, 3, -1), (5, 3, -3), (5, 4, -3)]
    print(difference_constraints(constraints2))
