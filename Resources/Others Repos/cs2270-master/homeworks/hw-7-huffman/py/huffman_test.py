import unittest
from RetroPrinter import RetroPrinter
from sys import argv

from huffman import *

class RetroTest(unittest.TestCase):

    def __init__(self, methodName, outputName):
        super(RetroTest, self).__init__(methodName) # call superconstructor
        self.outputName = outputName

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # then a bunch of test functions. asserts left here for copy/paste
    def test_tree_supernode(self):
        childA = init_freq_info_leaf('a', 0.3)
        childB = init_freq_info_leaf('b', 0.4)
        parent = init_freq_info_supernode(childA, childB)
        self.assertTrue(are_same(parent.freq, childA.freq + childB.freq))
        self.assertTrue(parent.left == childA and parent.right == childB)
        self.assertTrue(not parent.is_leaf)

    # then a bunch of test functions. asserts left here for copy/paste
    def test_huff_table(self):
        root = build_prefab_tree()
        self.assertTrue(root.freq == 36.0)
        table = build_encoding_map(root)
        self.assertTrue(len(table) == 16)
        # spot check some values
        exp = "..."
        self.assertTrue(table['e'] == exp)
        exp = ".^^."
        self.assertTrue(table['t'] == exp)
        exp = "^^..^";
        self.assertTrue(table['l'] == exp)

    # then a bunch of test functions. asserts left here for copy/paste
    def test_huff_tree(self):
        queue = read_corpus("../cpp/pkd.txt")
        tree = build_huffman_tree(queue)
        result = checkTree(tree)
        self.assertTrue(result)

    # then a bunch of test functions. asserts left here for copy/paste
    def test_encode(self):
        table = build_prefab_map()
        self.assertTrue(table['a'] == ".^.")
        inString = "aammttamt";
        result = encode(inString, table)
        exp = ".^..^..^^^.^^^.^^..^^..^..^^^.^^."
        self.assertTrue(result == exp)

    # then a bunch of test functions. asserts left here for copy/paste
    def test_decode(self):
        tree = build_prefab_tree()
        inString = ".^..^..^^^.^^^.^^..^^..^..^^^.^^."
        result = decode(inString, tree)
        exp = "aammttamt"
        self.assertTrue(result == exp)

    # then a bunch of test functions. asserts left here for copy/paste
    def test_sequence(self):
        queue = read_corpus("../cpp/pkd.txt")
        huffman_root = build_huffman_tree(queue)
        encoding_map = build_encoding_map(huffman_root)
  
        short_orig = "BREWED ON THE BANKS OF THE MIGHTY ST. VRAIN"
        medium_orig = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
        long_orig = "Four score and seven years ago our fathers brought forth on this continent a new nation, conceived in liberty, and dedicated to the propostion that all men are created equal. Now we are engaged in a great civil war, testing whether that nation, or any nation, so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this. But, in a larger sense, we can not dedicate, we can not consecrate, we can not hallow this ground. The brave men, living and dead, who struggled here, have consecrated it, far above our poor power to add or detract. The world will little note, nor long remember what we say here, but it can never forget what they did here. It is for us the living, rather, to be dedicated here to the unfinished work which they who fought here have thus far so nobly advanced. It is rather for us to be here dedicated to the great task remaining before us---that from these honored dead we take increased devotion to that cause for which they gave the last full measure of devotion---that we here highly resolve that these dead shall not have died in vain: that this nation, under God, shall have a new birth of freedom: and that government of the people, by the people, for the people, shall not perish from the earth."

        short_enc = encode(short_orig, encoding_map)
        short_rebuilt = decode(short_enc, huffman_root)
        self.assertTrue(short_rebuilt == short_orig)

        med_enc = encode(medium_orig, encoding_map)
        med_rebuilt = decode(med_enc, huffman_root)
        self.assertTrue(med_rebuilt == medium_orig)

        long_enc = encode(long_orig, encoding_map)
        long_rebuilt = decode(long_enc, huffman_root)
        self.assertTrue(long_rebuilt == long_orig)


EPSILON = 0.0001
def are_same(a, b):
    return abs(a - b) < EPSILON

def build_prefab_tree():
    e = init_freq_info_leaf('e', 4.0)     # 1
    a = init_freq_info_leaf('a', 4.0)     # 2
    space = init_freq_info_leaf(' ', 7.0) # 3
    n = init_freq_info_leaf('n', 2.0)     # 4
    t = init_freq_info_leaf('t', 2.0)     # 5
    m = init_freq_info_leaf('m', 2.0)     # 6
    i = init_freq_info_leaf('i', 2.0)     # 7
    h = init_freq_info_leaf('h', 2.0)     # 8
    s = init_freq_info_leaf('s', 2.0)     # 9
    f = init_freq_info_leaf('f', 3.0)     # 10
    o = init_freq_info_leaf('o', 1.0)     # 11
    u = init_freq_info_leaf('u', 1.0)     # 12
    x = init_freq_info_leaf('x', 1.0)     # 13
    p = init_freq_info_leaf('p', 1.0)     # 14
    r = init_freq_info_leaf('r', 1.0)     # 15
    l = init_freq_info_leaf('l', 1.0)     # 16
    
    ou = combine(o, u)
    xp = combine(x, p)
    rl = combine(r, l)
    nou = combine(n, ou)
    ixp = combine(i, xp)
    rlf = combine(rl, f)
    tm = combine(t, m)
    hs = combine(h, s)
    enou = combine(e, nou)
    atm = combine(a, tm)
    ixphs = combine(ixp, hs)
    rlf_space= combine(rlf, space)
    enouatm= combine(enou, atm)
    ixphsrlf_space= combine(ixphs, rlf_space)
    root = combine(enouatm, ixphsrlf_space)
    return root

def combine(left, right):
    parent = freq_info()
    parent.freq = left.freq + right.freq
    parent.left = left
    parent.right = right
    parent.is_leaf = False
    return parent

def build_prefab_map():
    ret = { }
    ret['a'] = ".^."
    ret['m'] = ".^^^"
    ret['t'] = ".^^."
    return ret

def checkTree(node):
    if node is None:
        return False
    
    if not node.is_leaf:
        if node.left is None or node.right is None:
            return False

    sum = node.left.freq + node.right.freq
    if sum != node.freq:
        return False
    ret = checkTree(node.left)
    if ret:
        ret = checkTree(node.right)
    return ret

if __name__ == '__main__':
    retro = False
    if (len(argv) > 1 and argv[1] == "--retrograde"):
        retro = True
    print "Retro mode: " + str(retro)
    suite = unittest.TestSuite()
    # now pair the above functions to the retrograde name
    tests = [
        RetroTest("test_tree_supernode", "HuffTreeSupernode"),
        RetroTest("test_huff_tree", "HuffTree"),
        RetroTest("test_huff_table", "HuffTable"),
        RetroTest("test_encode", "Encode"),
        RetroTest("test_decode", "Decode"),
        RetroTest("test_sequence", "AllInSequence"),
        ]
    for test in tests:
        suite.addTest(test)
    if retro:
        result = RetroPrinter()
        print "Running Python test suite..."
        suite.run(result)
        print "Done running Python test suite."
    else:
        runner = unittest.TextTestRunner()
        runner.run(suite)

