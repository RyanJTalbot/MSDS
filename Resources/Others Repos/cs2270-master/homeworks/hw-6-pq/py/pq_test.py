import unittest
from RetroPrinter import RetroPrinter
from sys import argv

from pq import *

class RetroTest(unittest.TestCase):

    def __init__(self, methodName, outputName):
        super(RetroTest, self).__init__(methodName) # call superconstructor
        self.outputName = outputName

    def setUp(self):
        self.pq = PriorityQueue()

    def tearDown(self):
        pass

    def test_everything(self):
        text = "Cat Video"
	self.pq.insert(text, 3)
	text = self.pq.peek()
	self.assertTrue(text == "Cat Video")
	text = "RTS Game Packet"
	self.pq.insert(text, 10)
	text = self.pq.peek()
	self.assertTrue(text == "RTS Game Packet")
	text = "PingAlive"
	self.pq.insert(text, 2)
	text = self.pq.peek()
	self.assertTrue(text == "RTS Game Packet")
	text = "Medical Packet"
	self.pq.insert(text, 11.5)
	text = self.pq.peek()
	self.assertTrue(text == "Medical Packet")  
	text = "Medical Packet"
	self.pq.insert(text, 12.5)
	text = self.pq.peek()
	self.assertTrue(text == "Medical Packet")  
	text = "Cat Video"
	self.pq.insert(text, 3)
	text = self.pq.peek()
	self.assertTrue(text == "Medical Packet")
	# the PQ table should look like this:
	# 2    Ping Alive
	# 3    Cat Video
	# 3    Cat Video
	# 10   RTS Game Packet
	# 11.5 Medical Packet
	# 12.5 Medical Packet
	text = self.pq.remove()
	self.assertTrue(text == "Medical Packet")
	text = self.pq.peek()
	self.assertTrue(text == "Medical Packet")
	text = self.pq.remove()
	self.assertTrue(text == "Medical Packet")
	text = self.pq.peek()
	self.assertTrue(text == "RTS Game Packet")  
	text = self.pq.remove()
	self.assertTrue(text == "RTS Game Packet")  
	text = self.pq.remove()
	self.assertTrue(text == "Cat Video")  
	text = self.pq.remove()
	self.assertTrue(text == "Cat Video")  
	text = self.pq.remove()
	self.assertTrue(text == "PingAlive")
        # self.assertIsNotNone("obviously ok", "failure msg")
        # self.assertEqual(42, 42, "failure msg")
        # self.assertIsNone(None, "failure msg")
        # self.self.assertTrue(True, "failure msg")
        # self.assertFalse(False, "failure msg")


if __name__ == '__main__':
    retro = False
    if (len(argv) > 1 and argv[1] == "--retrograde"):
        retro = True
    print "Retro mode: " + str(retro)
    suite = unittest.TestSuite()
    # now pair the above functions to the retrograde name
    tests = [
        RetroTest("test_everything", "Everything"),
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

