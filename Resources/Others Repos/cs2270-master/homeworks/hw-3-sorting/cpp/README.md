Sorting (C++)
===========

See the README that is one directory up for general info on the
assignment.


The functions all have a similar signature. Here's the declaration for
`quicksort`:

	void quicksort(vector<int> &data, int low_idx, int high_idx);

Some things to note for the C++ version: it uses a `vector` object to
contain data, and it uses the `&` modifier to the input vector to make
it a _reference parameter_. These are explained in turn:

Vector
---------

These functions use a standard C++ class called `vector`. The
`sorting.h` file includes this at the top. A `vector` is essentially
an intelligent list data structure, with methods that let you append,
insert, remove, push, pop, and query its data.

The angle-brackets following the token `vector` are part of the data
type declaration. `data` is a `vector` that contains `int`
elements. This additional syntax is necessary, because otherwise the
compiler doesn't know what kind of elements will be in the data
structure.

[Reference documentation for `vector`](http://www.cplusplus.com/reference/vector/vector/?kw=vector).

Pass By Reference
---------

The parameter `data` is passed by _reference_. This means that
whatever changes you make to the variable inside the function will be
visible in the calling context.

Say there are functions:

	vegas(int val) {
		val = 1234;
	}
	
	change_me(int &val) {
		val = 1234;
	}

... and we do the following:

	int x = 4;
	int y = 5;
	vegas(x);
	change_me(y);
	cout << x << " " << y << endl;
	
It prints `4 1234`. Whatever happens in `vegas` stays in
vegas. Whatever happens in `change_me` is persistent outside.

For more on this C++ feature see
[introduction to parameter passing modes](http://pages.cs.wisc.edu/~hasti/cs368/CppTutorial/NOTES/PARAMS.html).
