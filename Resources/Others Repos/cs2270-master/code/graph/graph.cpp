/*
   Graph.cpp

   This is your implementation file for the depth-first and
   breadth-first search assignment. All the documentation and
   instructions are in the header file.

   Your Name:

   Your Collaborators:

 */
#include <iostream>
#include <string>
#include <set>
#include "graph.hpp"

using namespace std;

Graph::Graph() {
  // graphs are undirected by default
  directed = false;
}

Graph::~Graph() {

}

vector<Node*> Graph::getNodes() {
  return nodes;
}

vector<Edge*> Graph::getEdges() {
  return edges;
}

int Graph::getClock() {
  return clock;
}

void Graph::addNode(Node& n) {
  nodes.push_back(&n);
}

void Graph::addEdge(Edge& e) {
  edges.push_back(&e);
}
 
void Graph::removeNode(Node& n) {
  for (vector<Node*>::iterator it = nodes.begin();
       it != nodes.end(); 
       it++) {
    if (&n == *it) {
      nodes.erase(it);
      break;
    }
  }
}
 
void Graph::removeEdge(Edge& e) {
  for (vector<Edge*>::iterator it = edges.begin();
       it != edges.end(); 
       it++) {
    if (&e == *it) {
      edges.erase(it);
      break;
    }
  }
}

void Graph::setDirected(bool val) {
  directed = val;
}

bool Graph::isDirected() {
  return directed;
}

set<Edge*> Graph::getAdjacentEdges(Node& n) {
  set<Edge*> ret;
  vector<Edge*>::iterator it = edges.begin();
  for (; it != edges.end(); it++) {
    Edge* edge = *it;
    if (edge->getStart() == &n) {
      ret.insert(edge);
    }
    if (!directed && edge->getEnd() == &n) {
      ret.insert(edge);
    }
  }
  return ret;
}

void Graph::clear() {
  clock = 0;
  // nodes is vector<Node*>
  //  for (size_t i = 0; i < nodes.size(); i++) {
  //    Node* n = nodes[i];
  //  }
  vector<Node*>::iterator it = nodes.begin();
  for (;it != nodes.end(); it++) {
    Node* n = *it;
    n->clear();
  }
  vector<Edge*>::iterator eit = edges.begin();
  for (;eit != edges.end(); eit++) {
    Edge* e = *eit;
    e->setType(UNDISCOVERED_EDGE);
  }
  
}

void Graph::tick(string message) {
  // optional debugging function
}

void Graph::dfs(Node& start) {
  // implement me. see header file for info.

// mark node gray
// E = edges related to node 
// for all edges e in E:
//     a = other end of e
//     if a is white:
//       dfs(a) ; recurse!
//   mark node black
  clock++; // clock = clock + 1
  start.setColor(GRAY, clock);
  set<Edge*> adj = getAdjacentEdges(start);
  set<Edge*>::iterator it = adj.begin();
  Edge* e;
  Node* other;
  int col, dt, ft, rk;
  for (; it != adj.end(); it++) {
    e = *it;
    if (e->getStart() == &start) {
      other = e->getEnd();
    } else {
      other = e->getStart();
    }
    other->getDiscoveryInformation(col, dt, ft, rk);
    if (col == WHITE) {
      other->setPredecessor(start);
      e->setType(TREE_EDGE);
      dfs(*other);
    } else if (col == GRAY) {
      e->setType(BACK_EDGE);
    } else if (col == BLACK) {
      bool ancest = other->isAncestor(start);
      if (ancest) {
	e->setType(FORWARD_EDGE);
      } else {
	e->setType(CROSS_EDGE);
      }
    }
  }
  clock = clock + 1;
  start.setColor(BLACK, clock);
}

void Graph::dfs(Node& start, Node& finish) {
  // implement me. see header file for info.
}

void Graph::bfs(Node& start) {
  // implement me. see header file for info.
}

void Graph::bfs(Node& start, Node& finish) {
  // implement me. see header file for info.
}

Node::Node(string s) {
  data = s;
}

Node::~Node() {
  // This is equivalent to the default destructor the compiler will
  // generate for you. As a rule of thumb, you only need to `delete`
  // member variables that were created with `new` inside this
  // class. So, you don't need to do anything here. It could have been
  // left out of the header/impl file entirely.
}

string Node::getData() {
  return data;
}

void Node::setRank(int r) {
  rank = r;
}

/**
 * Set the color to WHITE, the discovery/finish time and rank to -1,
 * and sets the predecessor to NULL.
 **/
void Node::clear() {
  this->color = WHITE; // color = WHITE. Same thing. Don't need 'this'.
  this->discovery_time = -1; 
  this->completion_time = -1;
  this->rank = -1;
  this->predecessor = NULL;
}

void Node::setColor(int search_color, int time) {
  color = search_color;
  if (color == BLACK) {
    completion_time = time;
  } else if (color == GRAY) {
    discovery_time = time;
  } else if (color == WHITE) {
    
  } else {
    cout << "BZZZT you passed in the wrong color." << endl;
  }
}

void Node::getDiscoveryInformation(int& color, int& disco_time, 
				   int& finish_time, int& bfs_rank) {
  // color is the parameter
  // this-> is the member variable
  color = this->color;
  disco_time = this->discovery_time; // this is not necessary :)
  finish_time = completion_time;
  bfs_rank = rank;
}

bool Node::isAncestor(Node& other) {
  if (predecessor == NULL) {
    return false;
  }
  if (&other == predecessor) {
    return true;
  }
  return predecessor->isAncestor(other);
}

void Node::setPredecessor(Node& other) {
  predecessor = &other;
}

Edge::Edge(Node& n1, Node& n2) {
  a = &n1;
  b = &n2;
  weight = 1.0;
}

Edge::~Edge() {
}

float Edge::getWeight() {
  return weight;
}

void Edge::setWeight(float val) {
  weight = val;
}

Node* Edge::getStart() {
  return a;
}

Node* Edge::getEnd() {
  return b;
}

int Edge::getType() {
  return type;
}

void Edge::setType(int edge_type) {
  type = edge_type;
}

string what(int& v) {
  // HINT: Make use of this debugging function!
  string ret = "Unknown";
  if (v == WHITE) {
    ret = "White";
  } else if (v == GRAY) {
    ret = "Gray";
  } else if (v == BLACK) {
    ret = "Black";
  } else if (v == UNDISCOVERED_EDGE) {
    ret = "Undiscovered";
  } else if (v == TREE_EDGE) {
    ret = "Tree";
  } else if (v == BACK_EDGE) {
    ret = "Back";
  } else if (v == FORWARD_EDGE) {
    ret = "Forward";
  } else if (v == CROSS_EDGE) {
    ret = "Cross";
  }
  return ret;
}

ostream &operator << (ostream& out, Graph graph) {
  out << graph.nodes.size() << " Nodes:" << endl;
  out << "[";
  for (vector<Node*>::iterator it = graph.nodes.begin(); it != graph.nodes.end(); it++) {
    Node* n = *it;
    out << *n << ", ";
  }
  out << "]" << endl;
  out << graph.edges.size() << " Edges:" << endl;
  out << "[";
  for (vector<Edge*>::iterator it = graph.edges.begin(); it != graph.edges.end(); it++) {
    Edge* e = *it;
    out << *e << ", ";
  }
  out << "]";
  return out;
}

ostream &operator << (std::ostream& out, Node node) {
  out << node.data << " color: " << node.color << " dt/ft: " << node.discovery_time << "/" << node.completion_time;
  return out;
}

ostream &operator << (std::ostream& out, Edge edge) {
  out << *edge.a << " -- " << *edge.b << " (" << edge.type << ")";
  return out;
}

