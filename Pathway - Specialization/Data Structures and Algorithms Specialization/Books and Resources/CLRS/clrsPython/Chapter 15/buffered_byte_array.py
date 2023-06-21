#!/usr/bin/env python3
# buffered_byte_array.py

# Introduction to Algorithms, Fourth edition
# Linda Xiao

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

# Contains both BufferedByteWriter and BufferedByteReader to read and write bits.

class BufferedByteWriter:

	def __init__(self, output_filename):
		"""Initialize a byte array to be written to compressed file.

		Argument:
		output_filename -- name of file to write to
		"""
		# Prepare to write bits.
		self.output_filename = output_filename
		self.byte_array = bytearray() 	# complete byte_array written to file
		self.current_byte = 0 	# bytes to be written
		self.num_written = 0 	# number of bits written out of a byte

	def write_bit(self, bit):
		"""Write a bit to a byte. Once the byte is constructed, add to byte array. """
		self.num_written += 1
		# Insert bit into correct position of byte.
		self.current_byte |= bit << (8 - self.num_written)
		if self.num_written == 8: 	# filled up byte
			self.byte_array.append(self.current_byte)
			# Reset. 
			self.num_written = 0
			self.current_byte = 0

	def close(self):
		"""Finish writing to a byte array. Write to the output file."""
		# Append potentially incomplete byte.
		if self.num_written > 0:
			self.byte_array.append(self.current_byte)
		# Write complete byte array to file.
		output_file = open(self.output_filename, "wb")
		output_file.write(self.byte_array)
		output_file.close()


class BufferedByteReader:

	def __init__(self, input_filename):
		"""Open the file to read and initialize indices.

		Arguments:
=		input_filename -- file to read from
		"""
		# Prepare to read bits. 
		self.input_file = open(input_filename, "rb")
		self.byte = ord(self.input_file.read(1))  # read the first byte
		self.bit_index = 0  # index within a byte

	def read_bit(self):
		"""Read one bit."""
		self.bit_index += 1
		# Read a bit from the correct index of the last byte read.
		bit = (self.byte >> (8 - self.bit_index)) & 1
		# After reading a whole byte, read another byte.
		if self.bit_index == 8:
			self.bit_index = 0
			self.byte = self.input_file.read(1)
			if self.byte:  # edge case when done reading
				self.byte = ord(self.byte)
		return bit

	def close(self):
		"""Close file that has been read."""
		self.input_file.close()
