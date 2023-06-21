#!/usr/bin/env python3
# print_table.py

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

def print_table(table, start_i, end_i, start_j, end_j, conversion_func=None, whole_table=False):
    """Print formatted values that are used in a table.

    Arguments:
    table -- matrix/table
    start_i -- index of the first row to print
    end_i -- index of the last row to print
    start_j -- index of the first column to print, relative to the row
    end_j -- index of the last column to print
    conversion_func -- conversion function for table entries, None if no conversion needed
    whole_table -- True if printing entire table, False if only upper triangle
    """

    if conversion_func is None:
        conversion_func = lambda x: x

    # Find number of digits of longest number
    max_num_digit = float('-inf')
    for i in range(start_i, end_i + 1):
        for j in range(start_j if whole_table else start_j + i - start_i, end_j + 1):
            string = str(conversion_func(table[i, j]))
            if len(string) > max_num_digit:
                max_num_digit = len(string)
    # Print out relevant elements of table.
    for i in range(start_i, end_i + 1):
        if not whole_table:
            for j in range(start_j, start_j + i - start_i):
                print(' ' * max_num_digit, end=" ")
        for j in range(start_j if whole_table else start_j + i - start_i, end_j + 1):
            string = str(conversion_func(table[i, j]))
            print(string.rjust(max_num_digit), end=" ")
        print()
