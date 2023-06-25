'''
Read this if you wonder how priority queues work 'out of the box' in
Python.
'''
from heapq import heappush, heappop

class thing:
    def __init__(self, f, n):
        self.freq = f
        self.name = n
        
    def __str__(self):
        return self.name + ": " + str(self.freq)

things = [ thing(6, "A"), thing(3, "B"), thing(9, "C"), thing(-4, "D"), thing(5, "E") ]

print "Initial out of sorts list..."
for t in things:
    print t

print "\nSorting..."

things = sorted(things, key= lambda doohicky: doohicky.freq)

for t in things:
    print t
print "\nResetting to out of order state."

things = [ thing(6, "A"), thing(3, "B"), thing(9, "C"), thing(-4, "D"), thing(5, "E") ]

print "\nAdding to a min-heap in a tuple of (priority, object)"
h = [] # the priority queue as a heap
for thing in things:
    heappush(h, (thing.freq, thing))

print "\nGoing to pop the tuples and print the 2nd element (the object)"
while len(h) > 0:
    print heappop(h)[1]
