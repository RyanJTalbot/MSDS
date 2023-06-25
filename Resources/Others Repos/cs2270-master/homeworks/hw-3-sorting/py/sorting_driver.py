import unittest
from RetroPrinter import RetroPrinter
from sys import argv
from collections import Counter
from random import randint, seed

from sorting import *

def get_random_data(how_many, upper_bound):
    numbers = []
    for i in range(how_many):
        r = randint(0, upper_bound)
        numbers.append(r)
    return numbers

def is_nondecreasing(data):
    ret = True
    if (len(data) > 1):
        prev = data[0]
        for num in data[1:]:
            if prev > num:
                ret = False
                break
            prev = num
    return ret



class RetroTest(unittest.TestCase):

    def __init__(self, methodName, outputName):
        super(RetroTest, self).__init__(methodName) # call superconstructor
        seed()
        self.outputName = outputName

    # def mknode(self, num):
    #     ret = bt_node()
    #     ret.data = num
    #     return ret

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_quicksort(self):
        input_data = get_random_data(1000, 500)
        input_data_orig = list(input_data)
        size_before = len(input_data)
        quicksort(input_data, 0, size_before-1)
        self.assertEqual(len(input_data), size_before,
                         "Quicksort changed the length of the list.")
        self.assertTrue(Counter(input_data) == Counter(input_data_orig),
                        "Lists do not contain the same data values")
        self.assertTrue(is_nondecreasing(input_data),
                        "'Sorted' list is not actually sorted.")

    def test_bubblesort(self):
        input_data = get_random_data(1000, 500)
        input_data_orig = list(input_data)
        size_before = len(input_data)
        bubblesort(input_data)
        self.assertEqual(len(input_data), size_before,
                         "Bubblesort changed the length of the list.")
        self.assertTrue(Counter(input_data) == Counter(input_data_orig),
                        "Lists do not contain the same data values")
        self.assertTrue(is_nondecreasing(input_data),
                        "'Sorted' list is not actually sorted.")

    def test_mergesort(self):
        input_data = get_random_data(1000, 500)
        input_data_orig = list(input_data)
        size_before = len(input_data)
        mergesort(input_data)
        self.assertEqual(len(input_data), size_before,
                         "Mergesort changed the length of the list.")
        self.assertTrue(Counter(input_data) == Counter(input_data_orig),
                        "Lists do not contain the same data values")
        self.assertTrue(is_nondecreasing(input_data),
                        "'Sorted' list is not actually sorted.")

    def test_mysterysort(self):
        input_data = get_random_data(1000, 500)
        input_data_orig = list(input_data)
        size_before = len(input_data)
        mystery_sort(input_data)
        self.assertEqual(len(input_data), size_before,
                         "Mergesort changed the length of the list.")
        self.assertTrue(Counter(input_data) == Counter(input_data_orig),
                        "Lists do not contain the same data values")
        self.assertTrue(is_nondecreasing(input_data),
                        "'Sorted' list is not actually sorted.")

if __name__ == '__main__':
    retro = False
    if (len(argv) > 1 and argv[1] == "--retrograde"):
        retro = True
    print "Retro mode: " + str(retro)
    suite = unittest.TestSuite()
    # now pair the above functions to the retrograde name
    tests = [
        RetroTest("test_quicksort", "QuickSort"),
        RetroTest("test_bubblesort", "BubbleSort"),
        RetroTest("test_mergesort", "MergeSort"),
        RetroTest("test_mysterysort", "MysterySort"),
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

