/**
 * BinarySearchTreeIntf.java
 *
 * This defines the functions you must implement for the Java version
 * of binary search trees. Edit a file 'BinarySearchTree.java' and
 * make it implement this interface. Use the 'BTNode' class.
 **/

public interface BinarySearchTreeIntf {

    /**
     * Returns the top-most node of the tree. If the tree is empty
     * this must return null. (This is necessary for unit testing).
     **/
    BTNode getRootNode();

    /**
     * Sets the root node of this tree to the provided BTNode. (This
     * is necessary for unit testing).
     **/
    void setRootNode(BTNode newRoot);

    /**
     * Initialize a bt_node with the given data, and two NULL
     * children.
     */
    BTNode initNode(int data);
    
    /**
     * Insert the new_node in a proper location in the tree.
     */
    void insert(BTNode newNode);
    
    /**
     * Insert a new node with the given data value similarly to
     * insert().
     */
    void insertData(int data);
    
    /**
     * Removes a node from the tree whose data value is the same as
     * the input.  If no node in the tree contains the given data,
     * this function has no effect.
     */
    void remove(int data);
    
    /**
     * Return true if any node in the tree contains the given data
     * value.
     */
    boolean contains(int data);
    
    /**
     * Searches through the tree for a node that contains the given
     * data value. If such a node is found, it is returned. Otherwise
     * this function returns null.
     */
    BTNode getNode(int data);
    
    /**
     * Return the size of the tree. In other words, it returns the
     * number of nodes that are reachable by traversing the tree
     * starting from the top. If the tree is empty, it returns zero.
     */
    int size();
    
    /**
     * Return an integer array representing the contents of this
     * binary tree. The order of the array elements are the same found
     * during an inorder traversal of the tree.
     */
    int[] toArray();

}
