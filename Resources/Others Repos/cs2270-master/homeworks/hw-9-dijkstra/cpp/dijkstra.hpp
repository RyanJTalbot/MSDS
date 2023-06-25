#ifndef __dijkstra_h__
#define __dijkstra_h__

#include <algorithm>
#include <cmath>
#include <functional>
#include <climits>
#include <queue>
#include <set>
#include <string>
#include <vector>

#include "UTFramework.h"

#define WHITE 1
#define GRAY 2
#define BLACK 3

#define UNDISCOVERED_EDGE 9
#define TREE_EDGE 10
#define BACK_EDGE 11
#define FORWARD_EDGE 12
#define CROSS_EDGE 13

using namespace std;

// forward declarations
class Node; 
class Edge; 
class TreeNode;
class Tree;

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
   * Resets node and edge data to prepare it for dfs, bfs, or other
   * algorithms.
   **/
  void clear();

  /**
   * Optional function to debug.
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
   * Perform Dijkstra's algorithm for finding the minimum path length
   * from the given start node to all other reachable nodes in the
   * graph.
   *
   * You don't need to clear things yourself. The driver will call
   * clear() first.
   *
   * Return the spanning tree that is rooted at the given start node,
   * with a path to all reachable nodes.
   **/
  Tree* dijkstra(Node* start);

  /**
   * Perform Dijkstra's algorithm like in the other version, but end
   * the algorithm when a definitive path length is found to the given
   * end node. Note that the end node might be unreachable.
   *
   * Return the spanning tree that was found during this search. Note
   * that when an answer is found for the path from start to end, the
   * algorithm stops, so the tree may be incomplete compared with what
   * is produced from the single-argument version of the dijkstra
   * function.
   **/
  Tree* dijkstra(Node* start, Node* end);

  /**
   * Is this graph a DAG or not? Return true if it is, false if not.
   *
   * Remember, DAG stands for *Directed* Acyclic Graph.
   **/
  bool isDAG();

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
  float path_distance; // Path distance from the start node to this
		       // node. Use this in Dijkstra's algo
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
   * the predecessor to NULL, and path_distance to 0.
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
   * Sets the predecessor node in the spanning tree. For DFS this is
   * the node we were on when we discovered other for the first
   * time. For Dijkstra this can change depending on the shortest
   * path.
   **/
  void setPredecessor(Node& other);

  /**
   * Returns the pointer to the current predecessor.
   **/
  Node* getPredecessor();

  float getPathDistance() const;

  void setPathDistance(float pd);

};

class Edge {
private:
  Node* a;
  Node* b;
  int type; // one of the edge types defined in graph.hpp
  float weight; // cost associated with this edge. default = 1
public:
  Edge(Node& n1, Node& n2);
  Edge(Node& n1, Node& n2, float w);
  ~Edge();
  int getType();
  Node* getStart();
  Node* getEnd();
  float getWeight(); // this is the edge distance
  void setWeight(float val);

  friend std::ostream &operator << (std::ostream& out, Edge edge);

  /**
   * Set the edge type to the given value (see edge type #define
   * statements above).
   **/
  void setType(int edge_type);  
};

/**
 * This is a comparator that looks at two node pointers. You can use
 * this with a priority_queue object. This is not strictly needed for
 * the assignment, but you can use it if you like. Google for
 * std::binary_function to see examples of how this is used.
 **/
struct NodeComparator : public std::binary_function<Node*, Node*, bool> {
  bool operator()(const Node* left, const Node* right) const {
    return left->getPathDistance() > right->getPathDistance();
  }
};

/**
 * This class is defined for you. You have to use it, but not write
 * any of its code.
 **/ 
class TreeNode {
public:
  TreeNode(Node* n);
  Node* node;
  vector<TreeNode*> children;
};

/**
 * This class is defined for you. You have to use it, but not write
 * any of its code.
 **/ 
class Tree {
private:
  TreeNode* root;
  vector<TreeNode*> members; // for linear lookup
  void print_tree(TreeNode* tn, int lvl);
public:
  TreeNode* find(Node* data);
  void update(Node* child, Node* old_parent, Node* new_parent); 
  void setRoot(Node* root);
  TreeNode* getRoot();
  void print_tree();// debugging
};

#endif

