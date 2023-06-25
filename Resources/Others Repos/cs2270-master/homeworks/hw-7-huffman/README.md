Huffman Codes
========

We often work with storing or transporting data. If we can compress
this data in a lossless way, we save money and time on disk space and
network traffic. _Huffman Encoding_ is a neat process where we reduce
the number of bits required to store individual components from some
alphabet, when the frequency those components appear is not evenly
distributed.

In English, there are common letters (e, m, s, t) and less common
letters (x, z, q). Huffman codes exploit this by letting us use short
bit patterns for common letters and longer ones for uncommon letters.

The examples you'll read about unanimously talk about encoding written
human languages, but it could just as easily be applied to _any_
system of communication where there is some alphabet of symbols (such
as the instructions used in a program).

The Wikipedia page on Huffman Encoding is good. So is
[this thing by Alex Allain](http://www.cprogramming.com/tutorial/computersciencetheory/huffman.html). There's
really no shortage of good resources.

What To Do For This Assignment
==========

The implementation file already has code that reads a text file and
populates a priority queue with a special structure called a
`freq_info`. These contain information about symbols and their
frequency. The structure is also suited for use in a binary tree. 

You will be responsible for forming a Huffman Tree using this priority
queue. 

Once you have a Huffman Tree, you will be able to _encode_ source
strings that use the same symbols that appear in the tree's
leaves. Encoding results in a bitstring, which we'll represent with
`.` for zero and `^` for one. 

The flip side is that you will also be able to _decode_ our weird
bitstrings into human-readable strings, using your same Huffman tree.

What To Turn In
=======

You only need to turn in `huffman.cpp`, and if you created a header
file, you can turn that in too. Just __don't touch the `huffman.h`
file__.
