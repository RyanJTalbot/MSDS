#ifndef __graph_h__
#define __graph_h__

#include <vector>
#include <set>
#include <string>

/* Node colors are described at the bottom of the file. */
#define WHITE 1
#define GRAY 2
#define BLACK 3

/* Edge types are described at the bottom of the file. */
#define UNDISCOVERED_EDGE 9
#define TREE_EDGE 10
#define BACK_EDGE 11
#define FORWARD_EDGE 12
#define CROSS_EDGE 13

using namespace std;

// forward declarations so Graph understands
class Node; 
class Edge; 

class Graph {
private:
  bool directed;
  vector<Node*> nodes;
  vector<Edge*> edges;
  // The next two vectors may be used in your search algorithms.
  vector<Edge*> search_edges;
  vector<Node*> search_nodes;
  // The clock can be used to set discovery/finish times
  int clock;
public:
  Graph();
  ~Graph();
  vector<Node*> getNodes();
  vector<Edge*> getEdges();
  int getClock();
  void addNode(Node& n);
  void addEdge(Edge& e);
  void removeNode(Node& n);
  void removeEdge(Edge& e);
  bool isDirected();
  void setDirected(bool val);
  set<Edge*> getAdjacentEdges(Node& n);
  friend std::ostream &operator << (std::ostream& out, Graph graph);

  /**
   * Resets all nodes to have WHITE color, with -1 discovery and
   * finish times and rank. Resets all edges to type
   * UNDISCOVERED_EDGE. Resets the clock to 0.
   **/
  void clear();

  /**
   * OPTIONAL debugging method. Use this after every time you
   * increment the clock. The clock should increment every time a Node
   * color changes to GRAY or BLACK. You might pass in a string to
   * describe what just happened. If you are having trouble, consider
   * using this function as a place to track your algorithm's
   * progress. Print out your graph on each tick. If you want to get
   * very fancy, you can output your graph in 'dot' format. This is
   * the same format we used in the B-Tree assignment for debugging.
   *
   * This function is 100% optional, though.
   **/
  void tick(string message);

  /**
   * Run a depth-first search from the indicated start node, and
   * explores all reachable nodes. This ignores unreachable
   * nodes. When this function returns, all explored nodes are colored
   * BLACK, all unreachable nodes are WHITE. All explored nodes have
   * correct discovery/exit time information. All edges have correct
   * edge types (unfollowed edges should remain UNDISCOVERED).
   *
   * For a DFS, mark nodes GRAY when we first discover them, and BLACK
   * when we exit (finish) them.
   **/
  void dfs(Node& start);

  /**
   * This function has the same requirements as the single-argument
   * version of `dfs`, except this one terminates after the target
   * node has been discovered. If found, the target node should be
   * marked GRAY on exit; if it is not found, it should remain WHITE.
   **/
  void dfs(Node& start, Node& target);

  /**
   * Run a breadth-first search starting from the indicated node. This
   * sets the 'rank' value on all nodes to something appropriate: -1
   * for unreachable nodes, 0 for the start node, 1 for nodes that are
   * one edge from the start node, and so forth.
   *
   * For a BFS, mark nodes GRAY when they are enqueued, and BLACK when
   * they are dequeued.
   **/
  void bfs(Node& start);

  /**
   * This function has the same requirements as the single-argument
   * version of `bfs`, except this one stops after the target node is
   * reached. If found, the target node should be marked BLACK, and its
   * rank should be correctly set on exit. If it is not found, the
   * target node should remain WHITE with a rank of -1.
   **/
  void bfs(Node& start, Node& target);
};

class Node {
private:
  string data;
  int color; // WHITE = unvisited; GRAY = visited; BLACK = complete
  int discovery_time; // time step when the node was discovered by search
  int completion_time; // time step when node was completely finished
  int rank; // Number of steps from source node in a BFS. 0 means it
	    // was the source node.
  Node* predecessor; // Points to the predecessor node in the spanning
		     // tree.

public:
  Node(string s);
  ~Node();
  string getData();
  void setData(string s);

  void setRank(int rank);

  friend std::ostream &operator << (std::ostream& out, Node node);

  // methods to implement:
  
  /**
   * Set the color to WHITE, the discovery/finish time and rank to -1,
   * and sets the predecessor to NULL.
   **/
  void clear();

  /**
   * Set the 'color' of a node. Be sure to set the appropriate time
   * variable depending on what the color is. If it is WHITE, this
   * should be equivalent to calling clear().
   **/
  void setColor(int search_color, int time);

  /**
   * Set the color, discovery time, and finish time to 'color',
   * 'disco_time', 'finish_time', and 'bfs_rank' respectively.
   *
   * 'disco_time' and 'finish_time' are only meaningful if the search
   * was dfs (though there is no reason to not use these for debugging
   * purposes).
   *
   * 'bfs_rank' is only meaningful if bfs was the most recent search.
   **/
  void getDiscoveryInformation(int& color, int& disco_time, 
			       int& finish_time, int& bfs_rank);

  /**
   * Tells you if the given node is reachable by traversing this
   * node's predecessor list. This is essentially like searching for
   * an item in a linked list. You can do this iteratively (with a
   * cursor) or recursively by calling isAncestor on non-null
   * predecessors.
   **/
  bool isAncestor(Node& other);

  /**
   * Sets the predecessor node in the spanning tree. The predecessor
   * node was the node that we were exploring when we first discovered
   * a node (e.g. it was WHITE when we found it).
   **/
  void setPredecessor(Node& other);

};

class Edge {
private:
  Node* a;
  Node* b;
  int type; // one of the edge types defined in graph.hpp
  float weight; // cost associated with this edge. default = 1
public:
  Edge(Node& n1, Node& n2);
  ~Edge();
  int getType();
  Node* getStart();
  Node* getEnd();
  float getWeight(); // weight is used later, not in this assignment
  void setWeight(float val);

  friend std::ostream &operator << (std::ostream& out, Edge edge);

  /**
   * Set the edge type to the given value (see edge type #define
   * statements above).
   **/
  void setType(int edge_type);
  
};

#endif


/*

  Node color tells us if we have discovered a node, if we're in the
  middle of finishing a node, or if we've finished a node. They are:

  WHITE: Node has not yet been reached by the search.

  GRAY: Node has been reached by the search but is not yet complete.

  BLACK: Node has been completely explored.


  Edge type tells us information about how the path was discovered
  during a depth-first search, and it also might give us valuable
  information about the shape of the graph. There are four kinds of
  edges, though it is not necessary to use all of them all of the
  time. They are:

  TREE: A tree edge from A to B indicates that B was discovered via A.

  BACK: A back edge from C to A indicates that A was discovered before
  C, and C was discovered while A was still being explored.

  FORWARD: A forward edge from A to C indicates that C was completely
  examined when we found it, and A is an ancestor of C in the DFS
  spanning tree.

  CROSS: A cross edge from A to C indicates the C was copmletely
  examined when we found it, and A is NOT an ancestor of C in the DFS
  spanning tree.

  These edge types are summarized graphically at
  http://en.wikipedia.org/wiki/Depth-first_search and does a much
  better job than words can do.

  To determine edge types, you need to use both the discovery
  information (the color of the ending node) and the predecessor
  information (to distinguish between Cross and Forward edges).

  Tree edges are when the end node is white.

  Back edges are when the end node is gray.

  Forward and cross edges are when the end node is black. If the start
  node is an ancestor of the end node, it is a forward edge. Otherwise
  it is a cross edge.

 */
