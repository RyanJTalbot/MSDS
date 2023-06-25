//
// These functions are what I intended to write during class. Sorry
// about my derpage there.
//

/**
 * Helper function for 'insert'. 
 **/
void insert_recursively(bt_node* top, bt_node* new_node) {
  if (new_node->data < top->data) {
    if (top->left == NULL) {
      top->left = new_node;
    } else {
      insert_recursively(top->left, new_node);
    }
  } else {
    if (top->right == NULL) {
      top->right = new_node;
    } else {
      insert_recursively(top->right, new_node);
    }
  }
}

/**
 * Insert the new_node in a proper location in the tree indicated by
 * *top_ref. On return, *top_ref points to the root of the tree.
 **/
void insert(bt_node** top_ref, bt_node* new_node) {
  if (*top_ref == NULL) {
    *top_ref = new_node;
  } else {
    insert_recursively(*top_ref, new_node);
  }
}
