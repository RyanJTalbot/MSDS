B-Tree Invariants
===========

Invariants are wonderful things. They are collections of simple (well,
usually simple) rules that tell us if a data structure or algorithm is
working correctly. You can think of them like a contract.

Unfortunately there are different lists of invariants for B-Trees
because they were not pinned down from the start. (This is OK, since
it led to development of other kinds of B-Trees.)

Some definitions:

1. `node` is a B-tree node that contains information about `keys` and
`children`.
2. `keys` are values used to keep data in order. For our assignment a
key is just an integer, but in practice they could be any number of
data types. They are used to divide the tree into subtrees.
3. `children` are references to other `nodes`. For this assignment
they are simply in-memory pointers. In a real situation they might be
disk addresses.
4. `root`: this is the top-most node of a B-Tree. Unlike the binary
trees we have seen, this may change due to inserting or removing
data. We make exceptions for the root node.
5. `index nodes`: these are nodes that are not `leaves` and not
`root`. It is called an _index_ because its purpose is to guide us to
the next layer down.
6. `leaves`: these are the nodes at the _bottom_ of the tree. They do
not have children.
7. `order`: the order of a B-Tree is the maximum number of children a
non-leaf may have. This is commonly denoted as `m` for some reason.

For this assignment we will adhere to the following invariants:

1. A node's keys are kept in ascending order, starting at index 0.
2. A node may have at most `m` children.
3. Index nodes have at least `round_up(m/2)` children. _By inference
   this means index nodes have at least `round_up(m/2)-1` keys._
4. If the root is not a leaf, it has at least two children.
5. All leaves are at the same level.
6. Non-leaf nodes with `k` children contain `k−1` keys.
7. The node pointed to by `child[i]` holds keys that are less than
   `key[i]`. The node pointed to by the final child pointer holds keys
   that are larger than the final key.
8. Leaves must have at least `round_up(m/2) - 1` keys.
9. The node's `num_keys` and `is_leaf` members accurately describe the
   number of keys and if the node is a leaf or not.

The `round_up` function is equivalent to the C++ `ceil` function: it
gives you the smallest integer that is equal to or greater than the
input. Examples:

	round_up(4/2) = round_up(2)   = 2
	round_up(5/2) = round_up(2.5) = 3
	round_up(6/2) = round_up(3)   = 3
	round_up(7/2) = round_up(3.5) = 4
