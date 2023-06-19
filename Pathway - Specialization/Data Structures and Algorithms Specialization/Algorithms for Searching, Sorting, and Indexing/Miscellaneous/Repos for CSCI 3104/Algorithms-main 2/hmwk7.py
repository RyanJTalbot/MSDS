

class Graph():

    def __init__(self, adjacency_matrix):
        """ 
        Graph initialized with a weighted adjacency matrix 
        
        Attributes
        ----------
        adjacency_matrix : 2D array
            non-negative integers where adjacency_matrix[i][j] is the weight of the edge i to j,
            with 0 representing no edge

        """

        self.adjacency_matrix = adjacency_matrix

        # Add more class variables below as needed, such as n:
        self.N = len(adjacency_matrix)
        
        
    def smallestEdge(self, edgeCost, mst): # Finds the vertex with the minimum distance
  
        smallest = 99999 # set it to super large number first for comparison
  
        for i in range(self.N): 
            if mst[i] == False and edgeCost[i] < smallest: 
                smallest = edgeCost[i] 
                lowestIndex = i
  
        return lowestIndex

    
    def Prim(self):
        """
        Use Prim-Jarnik's algorithm to find the length of the minimum spanning tree starting from node 0

        Returns
        -------
        int
            Weighted length of tree

        """
        
        cost = 0 # declare cost of MST to be returned later
        edgeCost = [99999] * self.N # used to find next min edge - set to infinity
        prev = [0] * self.N # need to store mst 
        prev[0] = -1 # first one doesn't have a "parent" since it's the root
        mst = [False] * self.N # keeps track of vertices already included in MST, set to false (not yet added)
        edgeCost[0] = 0 # first vertex assigned to zero
  
        z = 0
        while z < self.N:

            x = self.smallestEdge(edgeCost, mst) # Find next smallest dist not already in the mst
  
            mst[x] = True # Mark as true which adds it to the mst
              
            y = 0
            while y < self.N: 
                # continue if mst doesn't include all vertices 
                # make sure not zero so that it doesn't pick itself/edge not connected to anything
                if mst[y] == False and self.adjacency_matrix[x][y] < edgeCost[y] and self.adjacency_matrix[x][y] > 0: 
                    prev[y] = x
                    edgeCost[y] = self.adjacency_matrix[x][y] # updating cost of adjacent vertices
                    
                y += 1
                
            z += 1
        
        # Find the total cost of the MST built
        for k in range(1, self.N): 
            cost += self.adjacency_matrix[k][prev[k]]

        return cost
        return -1


#  Example use case:

G = Graph([[0, 10, 11, 33, 60],
           [10, 0, 22, 14, 57],
           [11, 22, 0, 11, 17],
           [33, 14, 11, 0, 9],
           [60, 57, 17, 9, 0]])

print("MST Cost G: ", G.Prim())
# assert G.Prim() == 41

H = Graph([[0, 17, 5, 0],
           [17, 0, 11, 8],
           [5, 11, 0, 6],
           [0, 8, 6, 0]])

print("MST Cost H: ",H.Prim())

I = Graph([[0, 2, 3, 0, 0],
           [2, 0, 15, 2, 0],
           [3, 15, 0, 0, 13],
           [0, 2, 0, 0, 9],
           [0, 0, 13, 9, 0]])

print("MST Cost I: ",I.Prim())

A = Graph([ [0, 10, 11, 33, 60],
[10, 0, 22, 14, 57],
[11, 22, 0, 12, 17],
[33, 14, 12, 0, 9],
[60, 57, 17, 9, 0]])

print("MST Cost A: ",A.Prim())
# result should be 19 for the graph H

