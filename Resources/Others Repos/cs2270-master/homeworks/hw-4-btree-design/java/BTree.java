/**
 * BTree.java
 *
 * This is the data structure and interface definition for
 * B-Trees. You shouldn't edit this file. Instead sub-class it in the
 * BTreeImpl.java file and override the abstract methods. You may also
 * create your own constructor if you like.
 *
 * BTW the 'final' keyword means you can't assign to a member after it
 * is initialized, nor can your override a 'final' method.
 **/
public abstract class BTree {

    /**
     * This is the node structure. The B-Tree contains a single root
     * (see the member variable 'root' below). All nodes in the tree
     * are accessable via that root node.
     *
     * You may subclass this if you like.
     **/
    public static class Node {
	protected int numKeys;
	protected int[] keys;
	protected boolean isLeaf;
	protected Node[] children;

	/**
	 * Create a new node with the appropriate number of key and
	 * child slots. 
	 **/
	public Node(int order) {
	    numKeys = 0;
	    keys = new int[order-1];
	    isLeaf = false;
	    children = new Node[order];
	}

	/**
	 * Public accessor to get the number of valid keys. This implies
	 * there are numKeys + 1 valid children unless this is a leaf.
	 **/
	public final int getNumKeys() {
	    return numKeys;
	}
	
	/**
	 * Gives the key array. See getNumKeys() for restrictions.
	 **/
	public final int[] getKeys() {
	    return keys;
	}
	
	/**
	 * Tells you if this is a leaf node. Leaf nodes are not allowed to
	 * contain children when an operation finishes.
	 **/
	public final boolean isLeaf() {
	    return isLeaf;
	}
	
	/**
	 * Gives the child array. See getNumKeys() and isLeaf() for
	 * restrictions.
	 **/
	public final Node[] getChildren() {
	    return children;
	}
    }

    // the 'root' and 'order' parameters are protected, meaning they
    // are available to subclasses. Your implementation should
    // reference them.
    protected Node root;
    protected final int order; 

    /**
     * Create a new BTree. Your subclass should ensure this is used.
     **/
    public BTree(int order) {
	this.order = order;
	this.root = null;
    }

    /**
     * Give access to the root. The testing code needs this.
     **/
    public final Node getRoot() {
	return root;
    }

    /**
     * What is the order of this B-Tree?
     **/
    public final int getOrder() {
	return order;
    }

    /**
     * -------------------------------------------- I N S E R T ---------
     *
     * Insert the given key into a b-tree rooted at 'root'.  If the
     * key is already contained in the btree this should do nothing.
     * 
     * On exit: 
     * -- the 'root' member should refer to the root of the
     *    tree. (the root may change when we insert or delete)
     * -- the btree referred to by 'root' is valid.
     **/
    abstract void insert(int key);

    /**
     * -------------------------------------------- R E M O V E ---------
     *
     * Remove the given key from a b-tree rooted at 'root'. If the key is
     * not in the btree this should do nothing.
     *
     * On exit:
     * -- the 'root' member should refer to the root of the
     *    tree. (the root may change when we insert or delete)
     * -- the btree pointed to by 'root' is valid.
     **/
    abstract void remove(int key);

    /**
     * ----------------------------------------- C O N T A I N S --------
     *
     * Return true if any node accessed from the given root node contains
     * the provided key value.
     **/
    abstract boolean contains(int key);

}

