/*
   dijkstra_driver.cpp

   No arguments gives you the pretty colorized mode:

   ./dijkstra_driver.cpp

   The "--manual" argument causes the 'manual' function to run instead
   of running any of the unit test code:

   ./dijkstra_driver --manual

   The "--retrograde" argument causes the driver to run exacly as it
   does on the server:

   ./dijkstra_driver --retrograde

   Feel free to edit this file's manual() function to run your own
   testing. I have some stuff there to start with, you can use that or
   not, it is up to you.

 */
#define EPSILON 0.0001

#include "dijkstra.hpp"

using namespace Thilenius;
using namespace std;

bool eq(float actual, float expected) {
  return fabs(actual - expected) < EPSILON;
}

bool has(vector<TreeNode*>& kids, Node* n) {
  bool ret = false;
  for (size_t i=0; i < kids.size(); i++) {
    if (kids[i]->node == n) {
	ret = true;
    }
  }
  return ret;
}

bool ok(Node* n, float exp_dist, Node* exp_par, bool complain) {
  bool good = true;
  if (n == NULL) {
    if (complain) {
      IsTrue("Null", n != NULL, "Shouldn't be null");
    }
    good = false;
  }
  if (n != NULL) {
    if (!eq(n->getPathDistance(), exp_dist)) {
      if (complain) {
	IsTrue("Distance", eq(n->getPathDistance(), exp_dist), "Wrong :(");
      }
      good = false;
    }
    if (n->getPredecessor() != exp_par) {
      if (complain) {
	IsTrue("Predecessor", n->getPredecessor() == exp_par, "Wrong :(");
      }
      good = false;
    }
  }
  if (complain && good) {
    IsTrue("Node OK", true, "");
  }
  return good;
}

Graph mkgraph1() {
  Graph graph;
  Node* a = new Node("a");
  Node* b = new Node("b");
  Node* c = new Node("c");
  Node* d = new Node("d");
  Node* e = new Node("e");
  Node* f = new Node("f");
  Node* g = new Node("g");

  Edge* ab = new Edge(*a, *b, 0.5);
  Edge* ac = new Edge(*a, *c, 1.4);
  Edge* bc = new Edge(*b, *c, 0.4);
  Edge* ae = new Edge(*a, *e, 3.0);
  Edge* ce = new Edge(*c, *e, 2.5);
  Edge* cd = new Edge(*c, *d, 1.5);
  Edge* dg = new Edge(*d, *g, 0.2);
  Edge* eg = new Edge(*e, *g, 0.3);
  Edge* df = new Edge(*d, *f, 0.1);
  
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

  graph.addNode(*a);
  graph.addNode(*b);
  graph.addNode(*c);
  graph.addNode(*d);
  graph.addNode(*e);
  graph.addNode(*f);
  graph.addNode(*g);
  graph.addNode(*h);

  graph.addEdge(* new Edge(*a, *b, 0.4));
  graph.addEdge(* new Edge(*a, *c, 0.3));
  graph.addEdge(* new Edge(*a, *d, 0.7));
  graph.addEdge(* new Edge(*b, *e, 0.8));
  graph.addEdge(* new Edge(*b, *f, 0.2));
  graph.addEdge(* new Edge(*c, *e, 0.4));
  graph.addEdge(* new Edge(*c, *f, 0.5));
  graph.addEdge(* new Edge(*c, *g, 0.3));
  graph.addEdge(* new Edge(*d, *f, 0.2));
  graph.addEdge(* new Edge(*d, *g, 0.6));
  graph.addEdge(* new Edge(*e, *h, 1.5));
  graph.addEdge(* new Edge(*f, *h, 1.0));
  graph.addEdge(* new Edge(*g, *h, 0.5));

  graph.setDirected(true);

  return graph;
}

Graph mkgraph3() {
  Graph graph;

  Node* a = new Node("a");
  Node* b = new Node("b");
  Node* c = new Node("c");
  Node* d = new Node("d");

  graph.addNode(*a);
  graph.addNode(*b);
  graph.addNode(*c);
  graph.addNode(*d);
  graph.addEdge(* new Edge(*a, *b, 3.5));
  graph.addEdge(* new Edge(*a, *c, 4.2));
  graph.addEdge(* new Edge(*b, *d, 4.7));
  graph.addEdge(* new Edge(*c, *d, 3.4));
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
  // ./dijkstra_driver --manual

  cout << "Manual Program Begin" << endl;
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

  Tree* tree = new Tree;
  tree->setRoot(a);
  tree->update(b, NULL, a); // a -> b. No prior parent
  tree->update(c, NULL, a); // a -> c
  tree->update(d, NULL, b); // b -> d

  tree->update(d, b, c); // c -> d. inform b.
  tree->print_tree();

  cout << "Manual Program End" << endl;
  
}

SUITE_BEGIN("Dijkstra on DAGs")

TEST_BEGIN("DetectDAG")
{
  Graph g1 = mkgraph1();
  IsTrue("G1", g1.isDAG(), "Incorrect");
  Node* b = find(g1, "b");
  Node* f = find(g1, "f");
  g1.addEdge(* new Edge(*f, *b));
  IsTrue("G1'", !g1.isDAG(), "Incorrect");

  Graph g2 = mkgraph2();
  IsTrue("G2", g2.isDAG(), "Incorrect");
  Node* h = find(g2, "h");
  Node* a = find(g2, "a");
  g2.addEdge(* new Edge(*h, *a));
  IsTrue("G2'", !g2.isDAG(), "Incorrect");

  Graph g3 = mkgraph3();
  IsTrue("G3", g3.isDAG(), "Incorrect");
  g3.setDirected(false);
  IsTrue("G3'", !g3.isDAG(), "Incorrect");

}TEST_END

TEST_BEGIN("Dijkstra General")
{
  {
    Graph g3 = mkgraph3();
    g3.clear();
    Node* a = find(g3, "a");
    Node* b = find(g3, "b");
    Node* c = find(g3, "c");
    Node* d = find(g3, "d");
    g3.dijkstra(a);
    bool good = true;
    good = ok(a, 0, NULL, false) && good;
    good = ok(b, 3.5, a, false) && good;
    good = ok(c, 4.2, a, false) && good;
    good = ok(d, 7.6, c, false) && good;
    if (!good) {
      ok(a, 0, NULL, true);
      ok(b, 3.5, a, true);
      ok(c, 4.2, a, true);
      ok(d, 7.6, c, true);
    } else {
      IsTrue("G3", true, "");
    }
  }

  {
    Graph g2 = mkgraph2();
    g2.clear();
    Node* a = find(g2, "a");
    Node* b = find(g2, "b");
    Node* f = find(g2, "f");
    Node* h = find(g2, "h");
    Node* g = find(g2, "g");
    Node* d = find(g2, "d");
    g2.dijkstra(a);
    ok(f, 0.6, b, true);
    ok(h, 1.1, g, true);
    ok(d, 0.7, a, true);
  }

  {
    Graph g1 = mkgraph1();
    g1.clear();
    Node* a = find(g1, "a");
    Node* b = find(g1, "b");
    Node* c = find(g1, "c");
    Node* d = find(g1, "d");
    Node* f = find(g1, "f");
    Node* g = find(g1, "g");
    Tree* tree = g1.dijkstra(a);
    ok(g, 2.6, d, true);
    ok(f, 2.5, d, true);
    ok(c, 0.9, b, true);
    if (tree == NULL) {
      IsTrue("MST Null?", tree != NULL, "Return tree should not be null");
    } else {
      TreeNode* tn_d = tree->find(d);
      if (tn_d == NULL) {
	IsTrue("Null TreeNode?", tn_d != NULL, "Should find D in tree");
      } else {
	bool has_g = has(tn_d->children, g);
	bool has_f = has(tn_d->children, f);
	IsTrue("Tree D Has G", has_g, "D's tree should have child G");
	IsTrue("Tree D Has F", has_f, "D's tree should have child F");
      }
    }
  }
}TEST_END

TEST_BEGIN("Dijkstra Targeted")
{
  {
    Graph g3 = mkgraph3();
    g3.clear();
    Node* a = find(g3, "a");
    Node* b = find(g3, "b");
    Node* c = find(g3, "c");
    Node* d = find(g3, "d");
    g3.dijkstra(a, d);
    bool good = true;
    good = ok(a, 0, NULL, false) && good;
    good = ok(b, 3.5, a, false) && good;
    good = ok(c, 4.2, a, false) && good;
    good = ok(d, 7.6, c, false) && good;
    if (!good) {
      ok(a, 0, NULL, true);
      ok(b, 3.5, a, true);
      ok(c, 4.2, a, true);
      ok(d, 7.6, c, true);
    } else {
      IsTrue("G3", true, "");
    }
  }
  {
    Graph g2 = mkgraph2();
    g2.clear();
    Node* a = find(g2, "a");
    Node* b = find(g2, "b");
    Node* c = find(g2, "c");
    Node* h = find(g2, "h");
    g2.dijkstra(a, c);
    ok(h, INT_MAX, NULL, true); 
    ok(b, 0.4, a, true);
  }
  {
    Graph g1 = mkgraph1();
    g1.clear();
    Node* a = find(g1, "a");
    Node* b = find(g1, "b");
    Node* c = find(g1, "c");
    Node* d = find(g1, "d");
    g1.dijkstra(a, c);
    ok(d, INT_MAX, NULL, true);
    ok(c, 0.9, b, true);
    ok(b, 0.5, a, true);
    ok(a, 0, NULL, true);
  }
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
