CS 2270 Spring 2013 Test 1 Review
================

The first test is worth **40 points** and accounts for approximately
**12%** of your final grade. This test will cover the following
topics:

* Data Structure and Algorithm Design
* Debugging
* Pointers
* Recursion
* Computational Complexity
* Linked Lists
* Binary Search Trees
* Sorting Algorithms

Below are some sample questions. These are slightly harder than what
will appear on the test.

Design
=====

Design an algorithm that creates a copy of a binary tree, but with the
inorder search traversal reversed. For example, if the input tree has
inorder traversal order [3, 7, 9, 9, 10, 15], the resulting tree
should have traversal order [ 15, 10, 9, 9, 7, 3 ]. Note that this is
a plain binary tree, __not__ a binary search tree.

You don't need to write C++. Just convince us that you can identify
the general strategy, what the main problems are, and so on. You
should be able to give this documentation to a fellow student, and it
should give them enough information so they can implement your design.

__(Yes, this is a fairly open-ended question. The design question will
be sort of like this. It should be pretty clear if you know how to
approach a problem like this or not.__)

Debugging
======

Assume we have a node structure that is defined like this:

	struct node {
	  node* next;
	  int value;
	};
	
There is a bug in the following code that causes a segmentation fault.

	1 int add_to_all(node** top_ref, int num) {
	2   node* cursor = *top_ref;
	3   do {
	4      cursor->value = cursor->value + num;
	5 	   cout << cursor->value << endl;
	6      cursor = cursor->next;
	7   } while (cursor != NULL);
	8 }
	
First, what does a segmentation fault mean? Where are some likely
places to look for bugs when you get a segfault?

Second, assume that we know that `top_ref` is not null. 
Identify the first line where a segmentation fault
could occur.

Pointers
========


Say we have the following code. (Note: the code is not _pointer_less,
but it _is_ pointless).

	void pointer_easy() {
	  int bob = 88;
	  int* pam = &bob;
	  int** joe = &pam;
      // spot
	}

Here's a chart with the variable's addresses already filled in. Supply
each variable's _value_ when the line with `// spot` is reached.

	----- address ---- value --
	bob    0x7ff        ? 
	pam    0xa60        ?
	joe    0xf04        ?

If for whatever reason we wanted to use the variable `joe` to retreive
print out `88`, what punctuation would we use below (where the `???`
is):

	cout << ??? << endl;

Fill in the correct data type (replacing the `???`):

	??? foo = &joe;
	
Recursion
======

Recursive number multiplication
--------

Write a recursive function that finds the product of the numbers
ranging from N to M. It should have the following prototype:

	int product(int low, int high);
	
If the user calls `product(3, 5)` the result is `60`, since that is `3 * 4 * 5`. If the user calls `product(3, 10)` the result is `3 * 4 * 5 * 6 * 7 * 8 * 9 * 10`, which happens to be `1814400`.

Recursive Linked List `size`
--------

Remember the linked list `size` function? If not, it looked like this:

	int size(node* root); // give size of list pointed to by 'root'.
	
In this question we will re-implement it using recursion.

First, write some English or pseudocode that outlines the important
aspects about this recursive size function. What does it take in? What
does it return? How do we control when and when not to recurse? Is
there _bad_ input that we need to watch out for? To get full points,
this should be a good enough description that an average CS 2270
student can use it to implement their own C++ version.

Second, write the actual syntactically correct C++ code that
implements the design from above.

Complexity
========

What is the computational complexity of the recursive `size` function
that you completely correctly implemented above?

Now suppose we have a binary tree data structure that has an added
invariant that each node stores the size of it's tree. If we have a
tree with 1873 nodes in it, how many nodes will we need to visit to
find the total size of the tree?

What is the computational complexity of this all-size-knowing tree?

Linked Lists
========

The standard one-direction linked list we implemented in class had
this node definition:

	struct node {
	  int data;    // data: the value of this node
	  node* next;  // next: pointer to the next node in the list, or NULL
			       // if this is the last node.
	};

A _doubly linked list_ is one that augments this node structure with a
reference to the previous node:

    node* prev;
	
If there is no previous node, it is NULL.
	
Suppose we are writing the `remove` operation for this doubly-linked
list. Given the following text diagrams of a starting condition, draw
a picture of what the linked list should look like after the node
indicated as `doomed_node` is removed. Use boxes and arrows to
indicate nodes and links. 


Case 1: removing a node in the middle somewhere.

    top_ref --> top --> node1 --> node2 --> doomed_node --> node4 --> NULL
	                          <--       <--             <--

Case 2: removing the last node.

    top_ref --> top --> node1 --> node2 --> doomed_node --> NULL
	                          <--       <--
							  
Case 3: removing the first node.

	top_ref --> top --> doomed_node --> node2 --> doomed_node --> NULL
	                                <--       <--

Write the code to handle case 1 only using the following function
prototype:

	remove_middle(node* doomed_node);

Binary Search Trees
========

One interesting property of a binary search tree is the _height_ of a
tree. This is interesting because we must (in the worst case scenario)
traverse all the way to the leaves of the tree to find a node, so we'd
like to know how deep we have to go.

Must we always traverse to a leaf to insert a value? _yes/no_

To remove a value? _yes/no_ (Note: the question asks if we must
**always** do this)

Suppose the maximum height of a plain binary search tree is 8
nodes. Does this mean that *every* leaf is 8 nodes deep?

Write the code that finds the sum of node values from the root node to
a given leaf node, assuming a standard binary search tree. Use the
following prototype:

	int get_path_sum(bt_node* root, bt_node* leaf);

Now say we are using an augmented binary search tree data structure
that also includes a reference to the parent node (much like the
doubly-linked list from above). Let's call this an `rb_node`:

	struct rb_node {
		rb_node* parent;
		rb_node* left;
		rb_node* right;
		int value;
	};

Now write the path sum function using this enhanced `rb_node`. You may
write a recursive or non-recursive function:

	int get_path_sum(rb_node* leaf);


Sorting Algorithms
===========

Buggy pseudocode for the bubble sort algorithm is as follows:

	bubble(data) {
		num_rounds = 0
		swapped = true
		while (not swapped) {
			num_rounds++
			for i=0, i < data.size, i++ {
				if data[i] > data[i+1] {
					swap cells i and i+1 in data
					swapped = true
				}
			}
		}
	}

First, find the bug and fix it.

Second, what will the value of num_rounds be when the `while` loop
exits, given the following input data:

	[ 4, 8, 10, 9 ]
	
Under which circumstances (if any) will the `bubble` function above
result in `num_rounds == 1`?

Is the above `bubble` function recursive? Why or why not?

We often use inefficient methods of sorting because it is easy to
program, and the inefficiencies are not important. Write a "sorting"
algorithm that takes an unsorted array and uses a binary tree to
produce a sorted array. Recall that our binary tree implementation had
a `to_array` function that filled an input array:

	void to_array(bt_node* top, int arr[]);
	
Your code should only take a few lines, and is not very esoteric at
all. You should be able to leverage the binary search tree's
properties for your nefarious purposes.

	...
	// 'data' is an integer array of size n
	// 'root' is the root node of an empty binary tree
	//
	//   (your code here)
	//
