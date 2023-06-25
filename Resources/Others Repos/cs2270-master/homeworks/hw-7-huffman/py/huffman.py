#
# huffman.py
#
# Huffman Encoding in Python.
#
# Some functions are already implemented for you. Others are
# optional. The required ones are grouped.
#
# Unlike previous Python versions of the homework, the functions you
# implement are not part of a class. 
#
# Your Name:
#
# Your Collaborators:

from heapq import heappush, heappop
from sys import stdout

LEFT_CHAR = '.'
RIGHT_CHAR = '^'

# ------------------------------------------------------- Done for you ----
class freq_info:
    symbol = None
    freq = 0.0
    left = None
    right = None
    is_leaf = False

    def __str__(self):
        if self.is_leaf:
            return str(self.symbol) + ": " + str(self.freq)
        else:
            return "[" + str(self.freq) + "]"

def init_freq_info_leaf(symbol, freq):
    ret = freq_info()
    ret.symbol = symbol
    ret.freq = freq
    ret.is_leaf = True
    return ret

def add_freq(c, data):
    if data.has_key(c):
        data[c] = data[c] + 1
    else:
        data[c] = 0

def read_corpus(filename):
    f = open(filename, 'r')
    pq = []
    freq = { } # char to int map
    for line in f:
        for ch in line:
            add_freq(ch, freq)
    add_freq('\n', freq)
    f.close()
    total = 0
    for k in freq:
        total = total + freq[k]

    print "Number of unique characters:", len(freq)
    print "Number of character instances:", total

    # now we know the total number so we can calculate frequency data.
    fsum = float(total)
    for k in freq:
        info = init_freq_info_leaf(k, freq[k] / fsum)
        heappush(pq, (info.freq, info))
    print "Read file:", filename
    return pq

def manual_driver():

    # 1. Create a priority queue of one-node trees using some big text
    # file. This gives you a priority queue containing freq_info
    # objects. These are meant to be used as nodes in a tree. At the
    # moment, they are all disconnected, so you have a forest of tiny
    # one-node seedlings.

    queue = read_corpus("../cpp/pkd.txt")
    # debug_queue(queue)

    # 2. Now do something like the following:
    #
    # while priority queue has more than one item: 
    
    # Pop top two items, A and B. They are lowest frequency nodes.
    # Create non-leaf node C who points to children A and B. C's
    # frequency is the sum of A and B's frequency.  Insert C back into
    # the priority queue. We are left with a single node in the
    # priority queue. This is the root node of our huffman encoding
    # tree. Retain a reference to that root node.

    huffman_root = build_huffman_tree(queue)
    debug_tree(huffman_root, 0)

    # 3. The leaf layer of the huffman tree contains symbols. The path
    # from root to a leaf is the huffman encoding for that leaf's
    # symbol. Every time a left child is followed, that corresponds to
    # a zero bit; right children are one bits.
    #
    # Traverse the tree and create a bitstring for each leaf. If the
    # path from the root to the leaf happens to be Left Left Right
    # Left, the bitstring for that leaf is 0010. Store these
    # bitstrings in a map. The resulting map use symbols for keys and
    # strings that use LEFT_CHAR for 0 and RIGHT_CHAR for 1
    # (right). By default these are '.' and '^' respectively:
    #
    # key   bitstring
    # ---------------
    #  a     .^.^
    #  b     ..^.^
    #  z     ^^.^..^
    #  %     .^^....^
    #  e     ^^.
    #
    # Notice that 'e' uses three bits while '%' uses 8. Think about
    # why this is awesome.

    encoding_map = build_encoding_map(huffman_root)
    debug_encoding_map(encoding_map)

    # 4. Now that we have a Map of symbols to bitstrings, we can use
    # it to encode text data. I'll give little sentences to encode.
    # For the output, we're using strings rather than actual bits so
    # (a) we can read and debug it more easily, and (b) so we don't
    # have to deal with chopping up individual bytes in memory (which
    # isn't the point of the exercise).

    short_string = "And no one sings me lullabyes..."

    medium_string = "We don't need no education.\nWe don't need no thought control.\nNo dark sarcasm in the classroom.\nTeacher leave those kids alone!\n"

    long_string = "The lunatic is on the grass.\nThe lunatic is on the grass.\nRemembering games and daisy chains and laughs.\nGot to keep the loonies on the path.\n\nThe lunatic is in the hall.\nThe lunatics are in my hall.\nThe paper holds their folded faces to the floor\nAnd every day the paper boy brings more.\n\nAnd if the dam breaks open many years too soon\nAnd if there is no room upon the hill\nAnd if your head explodes with dark forebodings too\nI'll see you on the dark side of the moon.\n\nThe lunatic is in my head.\nThe lunatic is in my head\nYou raise the blade, you make the change\nYou re-arrange me 'til I'm sane.\nYou lock the door\nAnd throw away the key\nThere's someone in my head but it's not me.\n\nAnd if the cloud bursts, thunder in your ear\nYou shout and no one seems to hear.\nAnd if the band you're in starts playing different tunes\nI'll see you on the dark side of the moon."

    short_encoded = encode(short_string, encoding_map)
    medium_encoded = encode(medium_string, encoding_map)
    long_encoded = encode(long_string, encoding_map)

    # 5.  After encoding some strings into your huffman coded 'bit'
    # string, you can use the decode function to get back the
    # original. The way you do this is to read the input character by
    # character, starting from the root of your huffman tree. When you
    # see LEFT_CHAR, you move left; a RIGHT_CHAR, move right. When you
    # reach a leaf node, you have found the coded character. Record
    # that character. Move back to the root and continue reading the
    # input string until it is complete. The sequence you read should
    # be the original message.
    
    redone_short = decode(short_encoded, huffman_root)
    redone_medium = decode(medium_encoded, huffman_root)
    redone_long = decode(long_encoded, huffman_root)
    
    # check short_string and redone_short (and similar) to see if
    # the encode/decode processes are working properly.

def debug_queue(queue):
    h = list(queue)
    while len(h) > 0:
        print heappop(h)[1]

def debug_tree(node, level):
    print "Debugging tree starting with node: " + str(node)
    # implement (optional)
    if node is None:
        return
    print "  " * level
    stdout.write("[")
    if node.is_leaf:
        stdout.write("Leaf: ")
        if node.symbol in string.printable:
            stdout.write("'" + node.symbol + "'")
        else:
            stdout.write("'?'")
        stdout.write(' ')
    stdout.write(str(node.freq))
    stdout.write("] ")
    level = level + 1
    debug_tree(node.left, level)
    debug_tree(node.right, level)
    level = level - 1

def debug_encoding_map(huffman_map):
    # implement (optional)
    print "Debugging encoding map..."
    for symbol in huffman_map:
        if symbol in string.printable:
            print "'" + symbol + "' => " + huffman_map[symbol]
        else:
            print "(?) => " + huffman_map[symbol]




# ------------------------------------------------------------
# -     The stuff you want to implement is below here        -
# ------------------------------------------------------------

def init_freq_info_supernode(left, right):
    ret = freq_info()
    # implement me. set the value's members to the proper values. be
    # sure to set the is_leaf member correctly.
    return ret

def build_huffman_tree(queue):
    root = None
    # implement me. set 'root' to something useful and return it.
    return root

def build_encoding_map(huffman_root):
    ret = { }
    # implement me. I suggest doing this recursively with another
    # function that takes a string for the current state of the
    # bitstring. read the Python documentation on 'string' to see how
    # to add and erase characters to/from the end of a string.
    return ret;

def encode(original, encoding_map):
    result = ""
    # implement me
    return result

def decode(encoded, huffman_root):
    result = ""
    # implement me
    return result

if __name__ == "__main__":
    manual_driver()
