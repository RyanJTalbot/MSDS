/**
 * This specifies the interface for a linked list should be
 * implemented in LinkedList.java. Use the given Node object (in
 * Node.java) to conform to classical linked list semantics (like in
 * the C++ version).
 *
 * Of course, there's java.util.List and friends. Don't import
 * anything in your implementation, don't use the collections API, or
 * anything sneaky like that.
 */
public interface LinkedListInterface {

    /**
     * Create a new Node, but do not modify this list. The returned
     * Node contains the provided number and has no next Node (it is
     * null).
    */
    public Node initNode(int data);
    
    /**
     * Create a String that represents this linked list, starting from
     * the first (if any) node. The returned String may be empty, or
     * it may only contain numbers and single spaces. E.g. "", " ", "4
     * 3 2" are valid, but "4, 3, 2" is not.
     **/
    public String report();

    /**
     * Append a node containing this number to the end of the list.
     */
    public void appendData(int data);

    /**
     * Append the provided node to the end of this list.
     */
    public void append(Node node);

    /**
     * Like appendData(), but this inserts the number into the list at
     * the given offset. For example, if the list starts as:
     *
     * 10 20 30 40
     *
     * and we insertData(2, 5), the resulting list will be:
     *
     * 10 20 5 30 40
     *
     * Also note that valid insertion indexes range from 0 to size(),
     * inclusive. This way, you can add to the beginning with an
     * offset of 0, and add to the end with an offset of size().
     */
    public void insertData(int offset, int data);

    /**
     *  Same as insertData, except the node has been created for us.
     */
    public void insert(int offset, Node node);

    /**
     * Removes the node at the given offset. E.g. if we start with:
     *
     * 10 20 30 40
     *
     * and we remove(2), the resulting list will be:
     *
     * 10 20 40
     *
     * Valid indices for removal are in the range 0 to size()-1,
     * inclusive. 
     */
    public void remove(int offset);

    /**
     * Inform us how many nodes are in this list.
     */ 
    public int size();

    /**
     * Inform us if there is a node that contains the specified value.
     */
    public boolean contains(int data);

}
