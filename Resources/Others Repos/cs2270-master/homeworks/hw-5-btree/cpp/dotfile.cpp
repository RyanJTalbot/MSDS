//
// dotfile.cpp
//
// I pulled these out of the unittest help file to draw attention to
// them. You can use this to print a tree, and it generates something
// like the contents of sample-btree-diagram.dot. Just copy/paste the
// graph output to a file that ends in .dot and open it with GraphViz
// or similar. This is a great way to visualize your tree.
//
// A fancier version might use an alternate output stream that writes
// to a file rather than cout.

string get_id_for_dot(btree* &node) {
  stringstream ss;
  ss << node; // address in memory
  string as_addr = ss.str();
  as_addr.replace(0, 2, "BT_");
  return as_addr;
}

string get_label_for_dot(btree* &node) {
  stringstream ss;
  for (int i=0; i < node->num_keys; i++) {
    ss << "" << node->keys[i];
    if (i+1 < node->num_keys) {
      ss << " ";
    }
  }
  return ss.str();
}

void print_dot_label(btree* &node) {
  cout << "    " << get_id_for_dot(node) 
       << " [label=\"" << get_label_for_dot(node) << "\"];" << endl;
}

void print_graphviz_dotfile(btree* &node, int depth) {
  string spaces = "    ";
  if (depth == 0) {
    print_dot_label(node);
  }
  int idx = 0;
  string my_id = get_id_for_dot(node);
  for ( ; idx < node->num_keys; idx++) {
    if (!node->is_leaf) { // don't recurse if this is a leaf.
      print_dot_label(node->children[idx]);
      cout << spaces << my_id << " -- " << get_id_for_dot(node->children[idx]) << ";" << endl;
      print_graphviz_dotfile(node->children[idx], depth + 1);
    }
  }
  // there is always one leftover child, assuming it is not a leaf.
  if (!node->is_leaf) {
    print_dot_label(node->children[idx]);
    cout << spaces << my_id << " -- " << get_id_for_dot(node->children[idx]) << ";" << endl;
    print_graphviz_dotfile(node->children[idx], depth + 1);    
  }
}


void print_tree(btree* &root) {
  cout << "graph btree {" << endl;
  int depth = 0;
  print_graphviz_dotfile(root, depth);
  cout << "}" << endl;
}
