/*
   graph_driver.cpp

   This is the driver for the graph assignment on breadth-first and
   depth-first search. There are three ways to run this.

   No arguments gives you the pretty colorized mode:

   ./graph_driver.cpp

   The "--manual" argument causes the 'manual' function to run instead
   of running any of the unit test code:

   ./graph_driver --manual

   The "--retrograde" argument causes the driver to run exacly as it
   does on the server:

   ./graph_driver --retrograde

   Feel free to edit this file's manual() function to run your own
   testing. I have some stuff there to start with, you can use that or
   not, it is up to you.

 */
#include "UTFramework.h"
#include "graph.hpp"

using namespace Thilenius;
using namespace std;

Graph mkgraph() {
  Graph graph;
  Node* a = new Node("a");
  Node* b = new Node("b");
  Node* c = new Node("c");
  Node* d = new Node("d");
  Node* e = new Node("e");
  Node* f = new Node("f");
  Node* g = new Node("g");

  Edge* ab = new Edge(*a, *b);
  Edge* ac = new Edge(*a, *c);
  Edge* bc = new Edge(*b, *c);
  Edge* ae = new Edge(*a, *e);
  Edge* ce = new Edge(*c, *e);
  Edge* cd = new Edge(*c, *d);
  Edge* dg = new Edge(*d, *g);
  Edge* eg = new Edge(*e, *g);
  Edge* df = new Edge(*d, *f);
  Edge* fb = new Edge(*f, *b);
  // if graph is undirected, these could cause trouble. see that it doesn't
  Edge* gd = new Edge(*g, *d);
  Edge* ge = new Edge(*g, *e);
  
  graph.addNode(*a);
  graph.addNode(*b);
  graph.addNode(*c);
  graph.addNode(*d);
  graph.addNode(*e);
  graph.addNode(*f);
  graph.addNode(*g);
  
  graph.addEdge(*ab);
  graph.addEdge(*ac);
  graph.addEdge(*bc);
  graph.addEdge(*ae);
  graph.addEdge(*ce);
  graph.addEdge(*cd);
  graph.addEdge(*dg);
  graph.addEdge(*eg);
  graph.addEdge(*df);
  graph.addEdge(*fb);
  graph.addEdge(*gd);
  graph.addEdge(*ge);

  graph.setDirected(true);

  return graph;
}

Graph mkgraph2() {
  Graph graph;

  Node* a = new Node("a");
  Node* b = new Node("b");
  Node* c = new Node("c");
  Node* d = new Node("d");
  Node* e = new Node("e");
  Node* f = new Node("f");
  Node* g = new Node("g");
  Node* h = new Node("h");

  Edge* ab = new Edge(*a, *b);
  Edge* bc = new Edge(*b, *c);
  Edge* cd = new Edge(*c, *d);
  Edge* db = new Edge(*d, *b);
  Edge* ae = new Edge(*a, *e);
  Edge* ah = new Edge(*a, *h);
  Edge* ef = new Edge(*e, *f);
  Edge* fc = new Edge(*f, *c);
  Edge* fg = new Edge(*f, *g);
  Edge* fh = new Edge(*f, *h);

  graph.addNode(*a);
  graph.addNode(*b);
  graph.addNode(*c);
  graph.addNode(*d);
  graph.addNode(*e);
  graph.addNode(*f);
  graph.addNode(*g);
  graph.addNode(*h);

  graph.addEdge(*ab);
  graph.addEdge(*bc);
  graph.addEdge(*cd);
  graph.addEdge(*db);
  graph.addEdge(*ae);
  graph.addEdge(*ah);
  graph.addEdge(*ef);
  graph.addEdge(*fc);
  graph.addEdge(*fg);
  graph.addEdge(*fh);

  graph.setDirected(true);

  return graph;
}

Node* find(Graph& graph, string label) {
  for (size_t i = 0; i < graph.getNodes().size(); i++) {                        
    Node* n = graph.getNodes()[i];
    if (n->getData() == label) {
      return n;
    }
  }
  return NULL;
}

void manual() {
  // to run the manual tester just run
  // ./graph_driver --manual
  // I'm going to leave this in here for your inspiration
  cout << "Graph Program Begin" << endl;
  Graph graph = mkgraph2();
  graph.clear();
  Node* a = find(graph, "a");
  Node* e = find(graph, "e");
  graph.dfs(*a, *e);
  cout << graph << endl;
  for (vector<Node*>::iterator it = graph.getNodes().begin(); 
       it != graph.getNodes().end(); it++) {
    Node* node = *it;
    int ncolor, ndt, nft, nrank;
    node->getDiscoveryInformation(ncolor, ndt, nft, nrank);
    cout << "Node: " << *node << endl;
  }
  for (vector<Edge*>:: iterator it = graph.getEdges().begin();
       it != graph.getEdges().end(); it++) {
    Edge* edge = *it;
    cout << "Edge: " << *edge << endl;
  }
  cout << "Graph Program End" << endl;
}

SUITE_BEGIN("Graphs")

TEST_BEGIN("Clear")
{
  Graph graph = mkgraph();
  graph.clear();
  int color;
  int disco_time;
  int finish_time;
  int bfs_rank;
  bool bad = false;
  for (size_t i = 0; i < graph.getNodes().size(); i++) {
    Node* n = graph.getNodes()[i];
    if (n == NULL) {
      IsTrue("Not Null", n != NULL, "Node is null");
    } else {
      n->getDiscoveryInformation(color, disco_time, 
				 finish_time, bfs_rank);
      bad = color != WHITE || disco_time != -1 || 
	finish_time != -1 || bfs_rank != -1;
      if (bad) {
	IsTrue("White", color == WHITE, "Node not white");
	IsTrue("Disco Reset", disco_time == -1, "Disco time not reset");
	IsTrue("Finish Reset", finish_time == -1, 
	       "Finish time not reset");
	IsTrue("BFS Rank", bfs_rank == -1, "BFS rank not reset");
	break;
      }
    }
  }
  if (!bad) {
    IsTrue("Nodes OK", true, "");
  }
  bad = false;
  for (size_t i=0; i < graph.getEdges().size(); i++) {
    Edge* edge = graph.getEdges()[i];
    if (edge == NULL) {
      IsTrue("Not Null", edge != NULL, "Edge is null");
    } else {
      int type = edge->getType();
      if (type != UNDISCOVERED_EDGE) {
	bad = true;
	IsTrue("Undiscovered Edge", type == UNDISCOVERED_EDGE, 
	       "Edge type is not reset");
	break;
      }
    }
  }
  if (!bad) {
    IsTrue("Edges OK", true, "");
  }
  IsTrue("Clock OK", graph.getClock() == 0, "Clock not reset");
}TEST_END

TEST_BEGIN("NodeInformation")
{
  // this tests setting the search information inside a node like the
  // color, discovery and finish time, rank, and predecessor
  Graph graph = mkgraph();
  graph.clear();
  Node* a = find(graph, "a");
  Node* e = find(graph, "e");
  int color;
  int disco_time;
  int finish_time;
  int bfs_rank;
  a->getDiscoveryInformation(color, disco_time, finish_time, bfs_rank);
  IsTrue("White", color == WHITE, "Not white");
  IsTrue("Negative Disco Time", disco_time < 0, "Not negative");
  IsTrue("Negative Finish Time", finish_time < 0, "Not negative");
  IsTrue("Negative BFS Rank", bfs_rank < 0, "Not negative");
  a->setColor(GRAY, 1);
  a->getDiscoveryInformation(color, disco_time, finish_time, bfs_rank);
  IsTrue("Gray", color == GRAY, "Not gray");
  IsTrue("DiscoFin Time", disco_time == 1, "Incorrect");
  a->setColor(BLACK, 2);
  a->getDiscoveryInformation(color, disco_time, finish_time, bfs_rank);
  IsTrue("Black", color == BLACK, "Not black");
  IsTrue("Finish Time", finish_time == 2, "Incorrect");
  a->setRank(10);
  a->getDiscoveryInformation(color, disco_time, finish_time, bfs_rank);
  IsTrue("BFS Rank", bfs_rank == 10, "Incorrect");
  a->setPredecessor(*e);
  IsTrue("Predecessor", a->isAncestor(*e), "Predecessor not set correctly");

}TEST_END

TEST_BEGIN("DFS")
{
  Graph graph = mkgraph();
  graph.clear();
  Node* a = find(graph, "a");
  graph.dfs(*a);
  IsTrue("Clock Moved", graph.getClock() > 0, "Clock did not move");
  int color, dt, ft, r;
  a->getDiscoveryInformation(color, dt, ft, r);
  IsTrue("Color", color == BLACK, "Node A should be black");
  bool bad;
  for (size_t i = 0; i < graph.getNodes().size(); i++) {
    Node* n = graph.getNodes()[i];
    n->getDiscoveryInformation(color, dt, ft, r);
    bad = color != BLACK || dt < 0 || ft < 0;
    if (bad) {
      IsTrue("Color", color == BLACK, "Color should be black");
      IsTrue("Disco Time", dt >= 0, "Disco Time should be nonnegative");
      IsTrue("Finish Time", ft >= 0, 
	     "Finish Time should be nonnegative");
      break;
    }
  }
  if (!bad) {
    IsTrue("Search Nodes OK", true, "");
  }
  
}TEST_END

TEST_BEGIN("DFSEdgeClassification")
{
  Graph graph = mkgraph2();
  graph.clear();
  Node* a = find(graph, "a");
  Node* b = find(graph, "b");
  Node* c = find(graph, "c");
  Node* d = find(graph, "d");
  Node* e = find(graph, "e");
  Node* f = find(graph, "f");
  Node* g = find(graph, "g");
  Node* h = find(graph, "h");

  graph.dfs(*a);

  int count = 0;
  for (size_t i = 0; i < graph.getEdges().size(); i++) { // C++ iterators I hate you
    Edge* edge = graph.getEdges()[i];
    if (edge->getStart() == a && edge->getEnd() == b) {
      IsTrue("A->B", edge->getType() == TREE_EDGE, "Incorrect :(");
      count++;
    } else if (edge->getStart() == b && edge->getEnd() == c) {
      IsTrue("B->C", edge->getType() == TREE_EDGE, "Incorrect :(");
      count++;
    } else if (edge->getStart() == c && edge->getEnd() == d) {
      IsTrue("C->D", edge->getType() == TREE_EDGE, "Incorrect :(");
      count++;
    } else if (edge->getStart() == d && edge->getEnd() == b) {
      IsTrue("D->B", edge->getType() == BACK_EDGE, "Incorrect :(");
      count++;
    } else if (edge->getStart() == a && edge->getEnd() == e) {
      IsTrue("A->E", edge->getType() == TREE_EDGE, "Incorrect :(");
      count++;
    } else if (edge->getStart() == a && edge->getEnd() == h) {
      IsTrue("A->H", edge->getType() == FORWARD_EDGE, "Incorrect :(");
      count++;
    } else if (edge->getStart() == e && edge->getEnd() == f) {
      IsTrue("E->F", edge->getType() == TREE_EDGE, "Incorrect :(");
      count++;
    } else if (edge->getStart() == f && edge->getEnd() == c) {
      IsTrue("F->C", edge->getType() == CROSS_EDGE, "Incorrect :(");
      count++;
    } else if (edge->getStart() == f && edge->getEnd() == g) {
      IsTrue("F->G", edge->getType() == TREE_EDGE, "Incorrect :(");
      count++;
    } else if (edge->getStart() == f && edge->getEnd() == h) {
      IsTrue("F->H", edge->getType() == TREE_EDGE, "Incorrect :(");
      count++;
    }
  }
  IsTrue("Correct Num Tests", 10 == count, "Incorrect :(");
}TEST_END

TEST_BEGIN("BFS")
{
  Graph graph = mkgraph();
  graph.clear();
  Node* a = find(graph, "a");
  graph.bfs(*a);
  Node* b = find(graph, "b");
  Node* c = find(graph, "c");
  Node* d = find(graph, "d");
  Node* e = find(graph, "e");
  Node* f = find(graph, "f");
  Node* g = find(graph, "g");
  int color, dt, ft, rank;
  a->getDiscoveryInformation(color, dt, ft, rank);
  IsTrue("Directed Rank A", rank == 1 || rank == 0, "Incorrect :(");
  int base_rank = rank;
  b->getDiscoveryInformation(color, dt, ft, rank);
  IsTrue("Directed Rank B", rank == base_rank + 1, "Incorrect :(");
  c->getDiscoveryInformation(color, dt, ft, rank);
  IsTrue("Directed Rank C", rank == base_rank + 1, "Incorrect :(");
  d->getDiscoveryInformation(color, dt, ft, rank);
  IsTrue("Directed Rank D", rank == base_rank + 2, "Incorrect :(");
  e->getDiscoveryInformation(color, dt, ft, rank);
  IsTrue("Directed Rank E", rank == base_rank + 1, "Incorrect :(");
  f->getDiscoveryInformation(color, dt, ft, rank);
  IsTrue("Directed Rank F", rank == base_rank + 3, "Incorrect :(");
  g->getDiscoveryInformation(color, dt, ft, rank);
  IsTrue("Directed Rank G", rank == base_rank + 2, "Incorrect :(");
}TEST_END

TEST_BEGIN("BFSUndirected")
{
  Graph graph = mkgraph();
  Node* a = find(graph, "a");
  Node* b = find(graph, "b");
  Node* c = find(graph, "c");
  Node* d = find(graph, "d");
  Node* e = find(graph, "e");
  Node* f = find(graph, "f");
  Node* g = find(graph, "g");
  graph.setDirected(false);
  graph.clear();
  graph.bfs(*a);

  int color, dt, ft, rank;
  a->getDiscoveryInformation(color, dt, ft, rank);
  IsTrue("Undirected Rank A", rank == 1 || rank == 0, "Incorrect :(");
  int base_rank = rank;
  b->getDiscoveryInformation(color, dt, ft, rank);
  IsTrue("Undirected Rank B", rank == base_rank + 1, "Incorrect :(");
  c->getDiscoveryInformation(color, dt, ft, rank);
  IsTrue("Undirected Rank C", rank == base_rank + 1, "Incorrect :(");
  d->getDiscoveryInformation(color, dt, ft, rank);
  IsTrue("Undirected Rank D", rank == base_rank + 2, "Incorrect :(");
  e->getDiscoveryInformation(color, dt, ft, rank);
  IsTrue("Undirected Rank E", rank == base_rank + 1, "Incorrect :(");
  f->getDiscoveryInformation(color, dt, ft, rank);
  IsTrue("Undirected Rank F", rank == base_rank + 2, "Incorrect :(");
  g->getDiscoveryInformation(color, dt, ft, rank);
  IsTrue("Undirected Rank G", rank == base_rank + 2, "Incorrect :(");
}TEST_END
SUITE_END

int main (int argc, char* argv[])
{	
  if (argc == 2 && argv[1] == string("--manual")) {
    manual();
  } else {
    UTFrameworkInit;
  }
}
