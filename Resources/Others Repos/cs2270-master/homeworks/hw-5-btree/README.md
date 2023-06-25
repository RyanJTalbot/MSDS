B-Trees
========

This assignment is on implementing B-Trees. Last week you did
design. This week you'll find that you probably aren't done designing
:)

As was the case last week, the purpose is to take on a very
complicated data structure, and proceed purposefully and
systematically according to a design that you create.

You will find these useful:

[B-Trees](http://cis.stvincent.edu/html/tutorials/swd/btree/btree.html)
by D. Carlson and I. Minerd at Saint Vincent College.

[B-Tree Chapter](http://zgking.com:8080/home/donghui/publications/books/dshandbook_BTree.pdf)
by D. Zhang. In Handbook of Data Structures and Applications,
D. P. Mehta, S. Sahni (editors), Chapman & Hall/CRC, ISBN
1-5848-8435-5, 2004.

There is also a section in the Shaffer book but it is short and
cryptic.

Using the Driver
--------

I've provided a driver for the C++ version. It only tests the
invariants and if your code works from a high level. You will need to
write your own tests for things like splitting and combining nodes.

You can generate a `dot` graph of an arbitrary b-tree using
`print_tree(btree*)` that is found in `btree_unittest_help.cpp`. Just
copy/paste and save the `graph { .. }` text to a file and open it
using something that can read `dot` files, like _GraphViz_.

Here are the trees used in the unit tests:

Empty Tree used in Insert1 and BulkRandom:

![Empty Tree](https://raw.github.com/johnsogg/cs2270/master/homeworks/hw-5-btree/graph-empty.png)

Full Leaf Root used in Insert2 and Remove1:

![Full Leaf Root](https://raw.github.com/johnsogg/cs2270/master/homeworks/hw-5-btree/graph-full-leaf-root.png)

Two Tier used in Insert3 and Remove2:

![Two Tier](https://raw.github.com/johnsogg/cs2270/master/homeworks/hw-5-btree/graph-two-tier.png)

Full Two Tier used in Insert4 and Remove3:

![Full Two Tier](https://raw.github.com/johnsogg/cs2270/master/homeworks/hw-5-btree/graph-full-two-tier.png)

Thin Three Tier used in Remove4:

![Thin Three Tier](https://raw.github.com/johnsogg/cs2270/master/homeworks/hw-5-btree/graph-thin-three-tier.png)

If you want you can execute the driver with the `--print-trees` flag
to generate the dot output on your own machine.

Grading
-------

This week's homework is graded by RetroGrade. You can get up to 30
points on this, but 100% is considered 15 points. So you could get
200% on this. After the due date, the score will be capped at 15
points.  _This means you will be able to complete the assignment until
the end of the semester._

Definitions:

* Starving node: a node with fewer keys than are allowed.
* Thin node: a node with exactly the smallest number of keys allowed.
* Full node: a node that has more keys than a thin node but isn't fat.
* Fat node: a node with more keys than are allowed.

The points will be allocated like this:

__contains__ = 4 points.

_insert_ and _remove_ have several levels of difficulty:

__insert (1)__: _Insert into an initially root node until it is full_:
3 points

__insert (2)__: _Insert into the root until it splits and adds another
level to the B-Tree_: 3 points

__insert (3)__: _Insert into a multi-layer tree until it splits but
does not need to add height._ 3 points

__insert (4)__: _Insert into a multi-layer tree until it splits and
causes the height to increase._ 3 points

__remove (1)__: _Remove a key from a full leaf_: 3 points

__remove (2)__: _Remove a key from a full non-leaf node_: 3 points

__remove (3)__: _Remove a key from a thin node that can borrow from a
full sibling_: 3 points

__remove (4)__: _Remove a key from a thin node with thin siblings_: 3
points

In addition to the above checks, there will also be a final test:

__bulk random__: _Handle many insertions and removals of randomly
chosen integers_: 2 points


What to Write and Turn In
----------

You will turn in the file btree.cpp.

You will almost certainly write a whole bunch of extra helper
functions to do things like split or combine nodes, or borrow and lend
keys. You can make your own header file to declare these functions,
but the only file that will be compiled is btree.cpp (because the
build system won't know how to make the other stuff).

So: you can write and turn in additional header files, and refer to
them from btree.cpp, but all your implementation has to be in
btree.cpp.

__Be aware__ that the testing framework on my end will expect each of
your `btree` structure members to be correct. This means if
`btree->num_keys` is 3, the testing framework will expect key slots 0,
1, and 2 to be valid; and child slots 0, 1, 2, and 3 to be valid. 

B-Tree Header File
--------

The header file is available in `cpp/btree.h`. You will notice that
there are only three functions in there.

It is up to you to test that all the invariants are intact after each
insert/remove operation. I suggest you take a look at the
`invariants.md` file and write some code that checks each of them, and
use that code as you test.

You will need to write many functions that are not specified in the
header file. You may write a separate header file and submit it along
with your implementation file. Just be sure you `#include` it in your
implementation file.



