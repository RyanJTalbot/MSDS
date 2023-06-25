
BTREE_ORDER = 5

class Node:
    num_keys = 0
    keys = []
    is_leaf = False
    children = []
    

class BTree:

    #: root should always refer to the topmost node
    root = None

    def insert(key):
        '''
        Insert the given key into a b-tree rooted at 'root'.  If the
        key is already contained in the btree this should do nothing.
        
        On exit: 
        -- the 'root' member should refer to the root of the
           tree. (the root may change when we insert or delete)
        -- the btree referred to by 'root' is valid.
        '''
        pass

    def remove(key):
        '''
        Remove the given key from a b-tree rooted at 'root'. If the
        key is not in the btree this should do nothing.
        
        On exit:
        -- the 'root' member should refer to the root of the
           tree. (the root may change when we insert or delete)
        -- the btree pointed to by 'root' is valid.
        '''
        pass

    def contains(key):
        '''
        Return true if any node accessed from the given root node
        contains the provided key value.
        '''
        pass

