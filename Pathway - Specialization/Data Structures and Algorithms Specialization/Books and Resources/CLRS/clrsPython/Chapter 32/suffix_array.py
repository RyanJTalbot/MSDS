#!/usr/bin/env python3
# suffix_array.py

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


def compute_suffix_array(T, n, conversion_func=ord):
    """
    Compute and return the suffix array for a text T.

    Arguments:
    T -- the text
    n -- length of T
    conversion_func -- mapping from text to decimal digit.  Default is ord,
	designed for text and pattern that are ASCII characters.  Use int for
	strings of decimal digits.

    Returns:
    The suffix array SA for T: if SA[i] = j, then the suffix T[j:] is the ith suffix of T
    in lexicographic order.
    """
    # Unlike in the textbook, the substr_rank list has elements that are tuples,
    # element 0 in the tuple corresponding to left_rank, element 1 to right_rank,
    # and element 2 to index.
    substr_rank = []
    for i in range(n-1):
        substr_rank.append((conversion_func(T[i]), conversion_func(T[i+1]), i))
    substr_rank.append((conversion_func(T[n-1]), -1, n-1))  # use -1 because of 0-origin indexing

    # To sort, use Python's built-in sorting function.  It compares tuples based on the values
    # in element 0, breaking ties based on the values in element 1.  If still a tie, the order
    # does not matter, though the sorting function will break further ties based on the values in element 2.
    substr_rank.sort()

    l = 2  # upper bound on the lengths of substrings sorted so far
    rank = [None] * n

    while l < n:  # while some second substring in a pair could be nonempty
        r = make_ranks(substr_rank, rank, n)  # make new ranks based on the list of sorted substring ranks

        substr_rank = []
        for i in range(n):
            if i + l < n:
                substr_rank.append((rank[i], rank[i + l], i))
            else:
                substr_rank.append((rank[i], -1, i))

        # Again, sort the tuples in substr_rank based on the values in element 0, breaking ties
        # based on the values in element 1.  If still a tie, the order does not matter.
        # Because all ranks within substr_rank are in a known range, -1 to n-1, use radix sort,
        # first sorting on element 1 (right_rank) and then on element 2 (left_rank).
        substr_rank = radix_sort(substr_rank, n, (1, 0), (-1, n-1))

        l *= 2  # double the lengths of substrings sorted so far

    SA = [element[2] for element in substr_rank]  # SA[i] = substr_rank[i][2] (i.e., substr_rank[i].index)
    return SA


def make_ranks(substr_rank, rank, n):
    """
    Give each substring in the sorted order its rank, from 0 to the number of unique
    substrings, minus 1, based on the values in substr_rank.

    Arguments:
    substr_rank -- a sorted list of ranks of tuples containing left_rank, right_rank, index
    rank -- a list of ranks to be filled in
    n -- length of substr_rank

    Returns:
    r -- the maximum rank assigned
    When this function returns, rank[i] is the rank of the ith substring represented in substr_rank.

    """
    # The first one always has rank 0.
    r = 0
    rank[substr_rank[0][2]] = r
    for i in range(1, n):
        # If the ranks of both substrings are the same as for the previous one, they get the same rank.
        # Otherwise, increment the rank.
        if substr_rank[i][0] != substr_rank[i-1][0] or substr_rank[i][1] != substr_rank[i-1][1]:
            r += 1
        rank[substr_rank[i][2]] = r

    return r


def radix_sort(a, n, indices, span):
    """Perform radix sort on a list of tuples or lists.  Does not operate in-place.

    Arguments:
    a -- the list of elements
    n -- length of a
    indices -- a tuple of indices into the indices of each element in a, giving the order in which to sort
    span -- a 2-tuple giving the minimum and maximum values seen in each element

    Returns:
    The sorted version of list a.
    """
    for index in indices:
        a = counting_sort(a, n, index, span)

    return a


def counting_sort(a, n, index, span):
    """
    Perform counting sort on a list of tuples or lists.  Does not operate in-place.
    Key property: the sort is stable.

    Arguments:
    a -- the list of elements
    n -- length of a
    index -- an index into each element in a, to determine values to sort on
    span -- a 2-tuple giving the minimum and maximum values seen in each element

    Returns:
    The sorted version of list a, based on the values at the index into each element in a.
    The sort is stable.
    """
    min_value = span[0]
    max_value = span[1]
    count = [0] * (max_value - min_value + 1)
    count[0] = -1   # adjust for 0-origin indexing

    # Get counts of values.
    for i in range(n):
        count[a[i][index] - min_value] += 1

    # Accumulate.
    for i in range(1, len(count)):
        count[i] += count[i-1]

    # Create a list for the sorted result, and place values in it.
    sorted_a = [None] * n
    i = n-1
    while i >= 0:
        sorted_a[count[a[i][index] - min_value]] = a[i]
        count[a[i][index] - min_value] -= 1
        i -= 1

    return sorted_a


def compute_lcp(T, SA, n):
    """Compute and return the LCP array (longest common prefix array) for a text.

    Arguments:
    T -- the text
    SA -- suffix array for T
    n -- length of T and SA

    Returns:
    LCP -- the LCP array.  LCP[i] is the length of the longest common prefix of
    T[SA[i]:] and T[SA[i-1]:] for i > 0.  Define LCP[0] = 0, since T[SA[0]] has
    no lexicographically smaller prefix.
    """
    rank = [None] * n
    LCP = [None] * n

    for i in range(n):
        rank[SA[i]] = i  # by definition
    LCP[0] = 0
    l = 0  # initialize length of LCP

    for i in range(n):
        if rank[i] > 0:
            j = SA[rank[i] - 1]  # T[j:] precedes T[i:] lexicographically
            m = max(i, j)
            while m + l < n and T[i + l] == T[j + l]:
                l += 1  # next character is in the common prefix
            LCP[rank[i]] = l  # length of LCP of T[j:] and T[i:]
            if l > 0:
                l -= 1  # peel off the first character of the common prefix

    return LCP


# Testing
if __name__ == "__main__":
    T = "ratatat"
    n = len(T)
    SA = compute_suffix_array(T, n)
    print(SA)  # should be 5, 3, 1, 0, 6, 4, 2
    LCP = compute_lcp(T, SA, n)
    print(LCP)  # should be 0, 2, 4, 0, 0, 1, 3

    T = "bippityboppityboo"
    n = len(T)
    SA = compute_suffix_array(T, n)
    print(SA)  # should be 0, 14, 7, 1, 11, 4, 16, 15, 8, 10, 3, 9, 2, 12, 5, 13, 6
    LCP = compute_lcp(T, SA, n)
    print(LCP)  # should be 0, 1, 2, 0, 1, 5, 0, 1, 1, 6, 1, 7, 0, 4, 0, 3

    T = "aaaaaa"
    n = len(T)
    SA = compute_suffix_array(T, n)
    print(SA)  # should be 5, 4, 3, 2, 1, 0
    LCP = compute_lcp(T, SA, n)
    print(LCP)  # should be 0, 1, 2, 3, 4, 5
