#!/usr/bin/env python3
# huffman.py

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

# Code to read in an ASCII text file and write out a compressed version of it,
# using Huffman coding.  Optionally also writes out a representation of the
# tree that represents the Huffman code so that the file can be decompressed.
# Decompresses the file using either the original Huffman tree or by rebuilding
# the Huffman tree from the file.

from min_heap_priority_queue import MinHeapPriorityQueue
from binary_search_tree import *
from buffered_byte_array import *


class HuffmanNode:

	def __init__(self, char=None, freq=0, left=None, right=None):
		"""Initialize character, frequency count, and children of a node.
		"""
		self.char = char
		self.freq = freq
		self.left = left
		self.right = right

	@staticmethod
	def get_key(x):
		"""Return frequency as key for min-priority queue."""
		return x.freq

	def is_leaf(self):
		"""Return True if the node is a leaf, False if not a leaf.
		Only leaves have a character."""
		return self.char is not None

	def __str__(self):
		"""Return the character in this node."""
		return self.char


class HuffmanTree:
	EOF_CHAR = chr(0)  # added to end of input file and then compressed

	def __init__(self, input_filename, compressed_filename, decompressed_file_name, huffman_code_filename=None):
		"""Construct a Huffman code tree for a given input file.  Save the names
		of the input file, compressed file, decompressed file, and an optional file
		containing a representation of the tree.

		Arguments: 
		input_filename -- name of input file to compress
		compressed_filename -- name of output compressed file
		decompressed_filename -- name of decompressed file
		huffman_code_filename -- optional name of file holding the Huffman code for the input file;
		if None, then no file created
		"""

		self.input_filename = input_filename
		self.compressed_filename = compressed_filename
		self.decompressed_filename = decompressed_file_name
		self.huffman_code_filename = huffman_code_filename

		# Construct frequencies of characters and form a Huffman tree.
		self.root = self.construct_tree(self.compute_freq(self.input_filename))

	@ staticmethod
	def compute_freq(filename):
		"""Compute frequency of each character. 

		Argument:
		filename -- name of input file to compress

		Returns:
		A dictionary mapping characters to their frequencies
		"""

		input_file = open(filename, "r")
		freq_dict = {}

		char = input_file.read(1)
		# Read the input file one character at a time.
		while char:
			if char in freq_dict:
				freq_dict[char] += 1  # have already seen this character
			else:
				freq_dict[char] = 1  # first time seeing this character
			char = input_file.read(1)

		input_file.close()

		freq_dict[HuffmanTree.EOF_CHAR] = 1  # add the EOF character to the dictionary

		return freq_dict	

	@staticmethod
	def construct_tree(freq_dict):
		"""Construct Huffman tree from a dictionary of char to freq.

		Argument:
		freq_dict -- dictionary of characters with their corresponding
		frequencies
		"""
		n = len(freq_dict)  # number of distinct characters

		# Insert the characters into a min-priority queue.
		queue = MinHeapPriorityQueue(HuffmanNode.get_key)  # key is frequency
		for char in freq_dict:
			queue.insert(HuffmanNode(char, freq_dict[char]))

		# Repeatedly (n-1 times) combine the two nodes with minimum frequency into a new node.
		for i in range(n-1):
			x = queue.extract_min()
			y = queue.extract_min()
			queue.insert(HuffmanNode(freq=x.freq + y.freq, left=x, right=y))

		return queue.extract_min()  # after combining n-1 nodes, the root has the lowest frequency

	def encode_chars(self):
		"""Given the Huffman tree, create a dictionary mapping characters
		to their Huffman codes.  The mapping for each character is a tuple giving
		the number of bits in its Huffman code and an integer whose leading bits
		are the Huffman code.  If a file of the Huffman tree is desired, write it out.

		Returns:
		The dictionary mapping characters to their Huffman codes.
		"""
		codes = {}
		codes = self.encode_chars_helper(codes, self.root, 0, 0)  # encode the Huffman tree

		# Special case: empty input file, so that the only character to output is self.EOF_CHAR.
		if len(codes) == 1:
			codes[self.EOF_CHAR] = (1, 0)

		if self.huffman_code_filename is not None:
			self.write_huffman_code_file()

		return codes

	def encode_chars_helper(self, codes, node, length=0, num=0):
		"""Given a subtree of the Huffman tree, create a dictionary mapping characters
		to their Huffman codes.  The mapping for each character is a tuple giving
		the number of bits in its Huffman code and an integer whose leading bits
		are the Huffman code.  If a file of the Huffman tree is desired, write it out.

		Arguments:
		codes -- dictionary of codes being built so far
		node -- root of a subtree of the Huffman tree
		length -- number of digits of Huffman code so far
		num -- integer representation of Huffman code being built

		Returns:
		The dictionary mapping characters to their Huffman codes.
		"""
		if node.is_leaf(): 	# leaves hold characters
			codes[node.char] = (length, num)
		else:  # extend the codes being built
			codes = self.encode_chars_helper(codes, node.left, length+1, num << 1)  # append 0 to left child's code
			codes = self.encode_chars_helper(codes, node.right, length+1, (num << 1) + 1)  # append 1 to right child's code

		return codes

	def write_huffman_code_file(self):
		"""Create the file representing the Huffman code tree.
		The nodes of the tree appear in preorder in the file.
		An internal node is represented by a single character '0'.
		A leaf is represented by two characters: a '1' followed by the character in the leaf."""
		huffman_code_file = open(self.huffman_code_filename, "w")
		self.write_huffman_code_file_helper(huffman_code_file, self.root)
		huffman_code_file.close()

	def write_huffman_code_file_helper(self, huffman_code_file, node):
		"""Write into a file a subtree of a Huffman code tree.

		Arguments:
		huffman_code_file -- the file being written, already open
		node -- root of the subtree
		"""
		if node.is_leaf():
			huffman_code_file.write('1' + node.char)  # just this leaf
		else:  # write the subtree in preorder
			huffman_code_file.write('0')
			self.write_huffman_code_file_helper(huffman_code_file, node.left)
			self.write_huffman_code_file_helper(huffman_code_file, node.right)

	def compress(self):
		"""Compress an input file with a Huffman code and write the compressed information to a file.
		Assumes that the Huffman tree for the input file has already been created and
		that self.root is the tree's root."""
		codes = self.encode_chars()  # from the Huffman tree, create the character codes

		input_file = open(self.input_filename, "r")

		# Because the output file is not a 1-1 mapping of characters to bytes,
		# need to write it one bit at a time.
		compressed_file = BufferedByteWriter(self.compressed_filename)

		# Read the input file one character at a time.
		char = input_file.read(1)
		while char:  # while there are more characters
			length, num = codes[char]
			for bit in range(length - 1, -1, -1):  # write one bit at a time
				compressed_file.write_bit((num >> bit) & 1)  # BufferedByteWriter writes bits one byte at a time
			char = input_file.read(1)

		input_file.close()

		# Add an encoded EOF character so that we know when to stop decoding.
		length, num = codes[self.EOF_CHAR]

		for bit in range(length - 1, -1, -1):  # write encoded EOF character
			compressed_file.write_bit((num >> bit) & 1)

		compressed_file.close()

	def recreate_tree(self):
		"""Recreate the Huffman tree from the file representing it.
		The nodes of the tree appear in preorder in the file.
		An internal node is represented by a single character '0'.
		A leaf is represented by two characters: a '1' followed by the character in the leaf."""
		huffman_code_file = open(self.huffman_code_filename, "r")

		# Create the root of the Huffman tree.
		leaf_indicator = huffman_code_file.read(1)
		if leaf_indicator == '1':
			# Special case: only one distinct character, and it's EOF_CHAR.
			char = huffman_code_file.read(1)
			self.root = HuffmanNode(char)  # no other nodes to create
		else:
			self.root = HuffmanNode()  # create the root
			self.recreate_tree_helper(huffman_code_file, self.root)  # and create the rest

		huffman_code_file.close()

	def recreate_tree_helper(self, huffman_code_file, parent):
		"""Recreate a subtree of the Huffman tree from the file representing it.
		The nodes of the tree appear in preorder in the file.
		An internal node is represented by a single character '0'.
		A leaf is represented by two characters: a '1' followed by the character in the leaf.

		Arguments:
		huffman_code_file -- file containing the representation of the Huffman tree, already open
		parent -- parent of the subtree being created
		"""
		# Create the left subtree of the parent.
		leaf_indicator = huffman_code_file.read(1)
		if leaf_indicator == '1':
			char = huffman_code_file.read(1)  # character in the leaf
			node = HuffmanNode(char)
			parent.left = node
		else:
			node = HuffmanNode()  # no character in an internal node
			parent.left = node
			self.recreate_tree_helper(huffman_code_file, node)  # create this node's subtree

		# Create the right subtree of the parent.
		leaf_indicator = huffman_code_file.read(1)
		if leaf_indicator == '1':
			char = huffman_code_file.read(1)  # character in the leaf
			node = HuffmanNode(char)
			parent.right = node
		else:
			node = HuffmanNode()  # no character in an internal node
			parent.right = node
			self.recreate_tree_helper(huffman_code_file, node)  # create this node's subtree

	def decompress(self):
		"""Decompress text that is compressed with a Huffman code, and write the
		decompressed text to a file.  The Huffman code tree either has root self.root
		or is represented in a file and is to be recreated."""

		if self.huffman_code_filename is not None:
			self.recreate_tree()  # otherwise, just use Huffman tree with root self.root

		current_node = self.root

		# Because the compressed file is not a 1-1 mapping of characters to bytes,
		# need to read it one bit at a time.
		compressed_file = BufferedByteReader(self.compressed_filename)
		decompressed_file = open(self.decompressed_filename, "w")

		# Read the compressed file one bit at a time.
		while True:
			if current_node.is_leaf():
				if current_node.char == self.EOF_CHAR:  # stop decoding?
					break
				else:
					decompressed_file.write(current_node.char)
					current_node = self.root  # start decoding another compressed character
			else:
				# Read in another bit and go left if 0, right if 1.
				bit = compressed_file.read_bit()
				if bit == 0:
					current_node = current_node.left
				else:
					current_node = current_node.right

		# Done writing to decompressed file and reading compressed file.
		decompressed_file.close()
		compressed_file.close()


# Testing
if __name__ == "__main__":

	# Small test case.
	tree1 = HuffmanTree("hello.txt", "hello_compressed.txt", "hello_decompressed.txt",
						"hello_code.txt")
	tree1.compress()
	tree1.decompress()

	# Giant test case.
	tree2 = HuffmanTree("moby-dick.txt", "moby-dick_compressed.txt", "moby-dick_decompressed.txt",
						"moby-dick_code.txt")
	tree2.compress()
	tree2.decompress()

	# Empty file test case.
	tree3 = HuffmanTree("empty.txt", "empty_compressed.txt", "empty_decompressed.txt",
						"empty_code.txt")
	tree3.compress()
	tree3.decompress()

	# 1-character file test case.
	tree4 = HuffmanTree("one_char.txt", "one_char_compressed.txt", "one_char_decompressed.txt",
						"one_char_code.txt")
	tree4.compress()
	tree4.decompress()
