Dijkstra's Algorithm
========

Consult lecture from April 8 for more info.

This assignment is based on the same code as last week. Specifically,
the graph, node, and edge classes all make a reprise, though you don't
have to have a complete implementation for it to work.

This week has three functions.

* One to test if an input graph is a DAG or not.

* Another runs Dijkstra's algorithm without a specific target.

* The last runs Dijkstra's algorithm _with_ a specific target.

Tree
------

Both versions of Dijkstra's return a `Tree*`, which is the minimum
spanning tree found during that algorithm. You'll need to consult the
code to see particularly how it works. 

As a hint: create a `Tree*` at the top of your algo, and keep it up to
date. Set the root, and then every new node you visit that isn't the
start node, make sure it is in the tree. You'll need to update it when
you discover a better path.

Priority Queue
--------

You need to use a priority queue of some sort. However, the STL
`priority_queue` may be inadequate by itself because you can't query
that datastructure to see if it contains something (which is part of
the algorithm).

Two possible strategies (there are more, I'm sure):

1. Use a set alongside your priority queue. Every time you add or
remove to the queue, add or remove to the set as well. Make use of the
`std::find` function (Google that to see what I mean).

2. Leave the STL priority queue alone and write your own. This doesn't
need to be hyper-efficient. It just needs to keep nodes in order so
the ones with low path distance are towards the front of the queue and
the infinite ones are at the end.

We'll do some coding on Wednesday so check this out in advance.

It should not be a terrible assignment, though.

