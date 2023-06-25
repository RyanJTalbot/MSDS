//
//  btree.h
//

// ----- N O T E -----
//
//       Please read ../invariants.md for specific instructions on
//       what constitutes a well-formed B-Tree.
//

#include <iostream>

#ifndef btree_h
#define btree_h

// The BTREE_ORDER definition sets the B-tree order (using the Knuth
// definition). This is the number of children the node can have. The
// number of keys is one less than this value.

#define BTREE_ORDER 5
using namespace std;

// Note that the keys and children arrays are OVERSIZED to allow for
// some approaches to work, where nodes are allowed to temporarily
// have too many keys or children. You do not have to use the extra
// slots if you don't want to. Don't take this as a subtle hint that I
// want you to do it this way.
// 
// A valid btree node can have at most:
//   BTREE_ORDER-1 keys.
//   BTREE_ORDER children.
struct btree {
    int num_keys;
    int keys[BTREE_ORDER];
    bool is_leaf;
    btree* children[BTREE_ORDER + 1];
};


// -------------------------------------------- I N S E R T ---------
//
// Insert the given key into a b-tree rooted at 'root'.  If the key is
// already contained in the btree this should do nothing.  
// 
// On exit: 
// -- the 'root' pointer should refer to the root of the
//    tree. (the root may change when we insert or delete)
// -- the btree pointed to by 'root' is valid.
void insert(btree* &root, int key);

// -------------------------------------------- R E M O V E ---------
//
// Remove the given key from a b-tree rooted at 'root'. If the key is
// not in the btree this should do nothing.
//
// On exit:
// -- the 'root' pointer should refer to the root of the
//    tree. (the root may change when we insert or delete)
// -- the btree pointed to by 'root' is valid.
void remove(btree* &root, int key);

// ----------------------------------------- C O N T A I N S --------
//
// Return true if any node accessed from the given root node contains
// the provided key value.
bool contains(btree* &root, int key);

#endif
