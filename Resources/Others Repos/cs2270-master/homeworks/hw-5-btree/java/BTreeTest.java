
// Note on the TemplateTest:
//
// You really only need to do two things:
//
// 1. Search/replace TemplateTest with the name of your test.
//
// 2. Implement a bunch of functions that start with test and end with
// the name of the test you want. The names should match those
// provided in ../description-common.json. For example if a test is
// FooThingWorks, your test function should be testFooThingWorks.
//
// Nothing else is required as long as you attach the RetroPrinter to
// your test runner.

import org.junit.Test;
import org.junit.Before;
import static org.junit.Assert.*;
import org.junit.runner.JUnitCore;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class BTreeTest {

    public static final int BTREE_ORDER = 5;

    public static void main(String[] args) {
	if (args.length > 0) {
	    new BTreeTest().manual();
	} else {
	    JUnitCore core= new JUnitCore();
	    core.addListener(new RetroPrinter());
	    core.run(BTreeTest.class);
	}
    }

    BTree btree;

    @Before
    public void init() {
	btree = new BTreeImpl(BTREE_ORDER);
    }

    @Test 
    public void testInsert1() {
	btree.root = build_empty();
	Invariants invar;
	invar = check_invariants(btree.getRoot(), true);
	assertTrue(!any_false(invar));

	btree.insert(10);
	invar = check_invariants(btree.getRoot(), true);
	assertTrue(!any_false(invar));
	assertTrue(private_contains(btree.getRoot(), 10));

	btree.insert(40);
	invar = check_invariants(btree.getRoot(), true);
	assertTrue(!any_false(invar));
	assertTrue(private_contains(btree.getRoot(), 40));

	btree.insert(30);
	invar = check_invariants(btree.getRoot(), true);
	assertTrue(!any_false(invar));
	assertTrue(private_contains(btree.getRoot(), 30));

	btree.insert(20);
	invar = check_invariants(btree.getRoot(), true);
	assertTrue(!any_false(invar));
	assertTrue(private_contains(btree.getRoot(), 20));
    }

    @Test 
    public void testInsert2() {
	Invariants invar;

	btree.root = build_full_leaf_root();
	invar = check_invariants(btree.getRoot(), true);
	assertTrue(!any_false(invar));

	btree.insert(38);
	invar = check_invariants(btree.getRoot(), true);
	assertTrue(!any_false(invar));
	assertTrue(private_contains(btree.getRoot(), 38));	

	btree.root = build_full_leaf_root();
	btree.insert(25);
	invar = check_invariants(btree.getRoot(), true);
	assertTrue(!any_false(invar));
	assertTrue(private_contains(btree.getRoot(), 25));	

	btree.root = build_full_leaf_root();
	btree.insert(5);
	invar = check_invariants(btree.getRoot(), true);
	assertTrue(!any_false(invar));
	assertTrue(private_contains(btree.getRoot(), 5));	
    }

    @Test 
    public void testInsert3() {
	Invariants invar;
	btree.root = build_two_tier();
	invar = check_invariants(btree.getRoot(), true);
	assertTrue(!any_false(invar));
	btree.insert(16);
	assertTrue(!any_false(invar));
	assertTrue(private_contains(btree.getRoot(), 16));
    }

    @Test 
    public void testInsert4() {
	Invariants invar;
	CheckHeight result = new CheckHeight();
	btree.root = build_full_two_tier();
	invar = check_invariants(btree.getRoot(), true);
	assertTrue(!any_false(invar));
	check_height(btree.getRoot(), result);
	int height_before = result.result_height;
	btree.insert(19);
	invar = check_invariants(btree.getRoot(), true);
	assertTrue(!any_false(invar));
	check_height(btree.getRoot(), result);
	int height_after = result.result_height;
	assertTrue(height_before + 1 == height_after);
    }

    @Test 
    public void testRemove1() {
	Invariants invar;
	btree.root = build_full_leaf_root();
	btree.remove(20);
	invar = check_invariants(btree.getRoot(), true);
	assertTrue(!any_false(invar));
	assertFalse(private_contains(btree.getRoot(), 20));

	btree.remove(10);
	invar = check_invariants(btree.getRoot(), true);
	assertTrue(!any_false(invar));
	assertFalse(private_contains(btree.getRoot(), 10));

	btree.remove(40);
	invar = check_invariants(btree.getRoot(), true);
	assertTrue(!any_false(invar));
	assertFalse(private_contains(btree.getRoot(), 40));

	btree.remove(30);
	invar = check_invariants(btree.getRoot(), true);
	assertTrue(!any_false(invar));
	assertFalse(private_contains(btree.getRoot(), 30));
    }

    @Test 
    public void testRemove2() {
	Invariants invar;
	btree.root = build_two_tier();
	btree.remove(17);
	invar = check_invariants(btree.getRoot(), true);
	assertTrue(!any_false(invar));
	assertFalse(private_contains(btree.getRoot(), 17));
    }

    @Test 
    public void testRemove3() {
	Invariants invar;
	btree.root = build_full_two_tier();
	CheckHeight result = new CheckHeight();
	check_height(btree.getRoot(), result);
	int before = result.result_height;
	btree.remove(6);
	invar = check_invariants(btree.getRoot(), true);
	assertTrue(!any_false(invar));
	assertFalse(private_contains(btree.getRoot(), 6));
	check_height(btree.getRoot(), result);
	assertTrue(result.result_height == before);
    }

    @Test 
    public void testRemove4() {
	Invariants invar;
	btree.root = build_thin_three_tier();
	CheckHeight result = new CheckHeight();
	check_height(btree.getRoot(), result);
	int before = result.result_height;
	btree.remove(5);
	invar = check_invariants(btree.getRoot(), true);
	assertTrue(!any_false(invar));
	assertFalse(private_contains(btree.getRoot(), 5));
	check_height(btree.getRoot(), result);
	boolean height_reduced = before == result.result_height + 1;
	assertTrue(height_reduced);
    }

    @Test 
    public void testContains() {
	BTree empty = new BTreeImpl(BTREE_ORDER);
	empty.root = build_empty();
	BTree full_leaf = new BTreeImpl(BTREE_ORDER);
	full_leaf.root = build_full_leaf_root(); // 10, 20, 30, 40
	BTree two_tier = new BTreeImpl(BTREE_ORDER);
	two_tier.root = build_two_tier(); // 5 8 10 13 15 17 19 20 23 27 30 33 35 38

	assertTrue(!empty.contains(42));
	assertTrue(full_leaf.contains(10));
	assertTrue(full_leaf.contains(20));
	assertTrue(!full_leaf.contains(15));
	assertTrue(!full_leaf.contains(100));

	assertTrue(!two_tier.contains(18));
	assertTrue(!two_tier.contains(39));
	assertTrue(two_tier.contains(20));
	assertTrue(two_tier.contains(5));
	assertTrue(two_tier.contains(17));
	assertTrue(two_tier.contains(38));
    }

    @Test
    public void testBulkRandom() {
	Random rand = new Random(System.currentTimeMillis());
	List<Integer> numbers = new ArrayList<Integer>();
	for (int i =0 ; i < 400; i++) {
	    numbers.add(rand.nextInt(1000));
	}

	for (int i : numbers) {
	    btree.insert(i);
	    if (!btree.contains(i)) {
		assertTrue(btree.contains(i));
		break;
	    }
	}

	for (int i : numbers) {
	    btree.remove(i);
	    if (btree.contains(i)) {
		assertTrue(!btree.contains(i));
		break;
	    }
	}
	
    }

    BTree.Node build_empty() {
	BTree.Node ret = new BTree.Node(BTREE_ORDER, new int[] { }, true);
	return ret;
    }

    BTree.Node build_full_leaf_root() {
	BTree.Node ret = new BTree.Node(BTREE_ORDER, new int[] { 10, 20, 30, 40 }, true);
	return ret;
    }

    BTree.Node build_two_tier() {
	int valsRoot[] = { 10, 20, 30 };
	BTree.Node root = new BTree.Node(BTREE_ORDER, new int[] { 10, 20, 30 }, false);
	BTree.Node ch1 = new BTree.Node(BTREE_ORDER, new int[] { 5, 8 }, true);
	BTree.Node ch2 = new BTree.Node(BTREE_ORDER, new int[] { 13, 15, 17, 19 }, true);
	BTree.Node ch3 = new BTree.Node(BTREE_ORDER, new int[] { 23, 27 }, true);
	BTree.Node ch4 = new BTree.Node(BTREE_ORDER, new int[] { 33, 35, 38 }, true);
	root.getChildren()[0] = ch1;
	root.getChildren()[1] = ch2;
	root.getChildren()[2] = ch3;
	root.getChildren()[3] = ch4;
	return root;
    }


    BTree.Node build_full_two_tier() {
	BTree.Node root = new BTree.Node(BTREE_ORDER, new int[] { 4, 7, 13, 20 }, false);
	BTree.Node ch0 = new BTree.Node(BTREE_ORDER, new int[] { 1, 3 }, true);
	BTree.Node ch1 = new BTree.Node(BTREE_ORDER, new int[] { 5, 6 }, true);
	BTree.Node ch2 = new BTree.Node(BTREE_ORDER, new int[] { 8, 11, 12 }, true);
	BTree.Node ch3 = new BTree.Node(BTREE_ORDER, new int[] { 14, 16, 17, 18 }, true);
	BTree.Node ch4 = new BTree.Node(BTREE_ORDER, new int[] { 23, 24, 25, 26 }, true);
	root.getChildren()[0] = ch0;
	root.getChildren()[1] = ch1;
	root.getChildren()[2] = ch2;
	root.getChildren()[3] = ch3;
	root.getChildren()[4] = ch4;
	return root;
    }


    BTree.Node build_thin_three_tier() {
	BTree.Node root = new BTree.Node(BTREE_ORDER, new int[] { 13 }, false);
	BTree.Node ch0 = new BTree.Node(BTREE_ORDER, new int[] { 4, 7 }, false);
	BTree.Node ch1 = new BTree.Node(BTREE_ORDER, new int[] { 17, 24 }, false);

	root.getChildren()[0] = ch0;
	root.getChildren()[1] = ch1;

	BTree.Node l0 = new BTree.Node(BTREE_ORDER, new int[] { 1, 3 }, true);
  	BTree.Node l1 = new BTree.Node(BTREE_ORDER, new int[] { 5, 6 }, true);
  	BTree.Node l2 =  new BTree.Node(BTREE_ORDER, new int[] { 11, 12 }, true);

	ch0.getChildren()[0] = l0;
	ch0.getChildren()[1] = l1;
	ch0.getChildren()[2] = l2;
  
	BTree.Node r0 =  new BTree.Node(BTREE_ORDER, new int[] { 14, 16 }, true);
  	BTree.Node r1 =  new BTree.Node(BTREE_ORDER, new int[] { 19, 23 }, true);
  	BTree.Node r2 =  new BTree.Node(BTREE_ORDER, new int[] { 25, 26 }, true);
  
	ch1.getChildren()[0] = r0;
	ch1.getChildren()[1] = r1;
	ch1.getChildren()[2] = r2;

	return root;
    }

    String get_id_for_dot(BTree.Node node) {
	return "BT_" + node.hashCode();
    }

    public void manual() {
	BTree.Node empty = build_empty();
	BTree.Node full_leaf_root = build_full_leaf_root();
	BTree.Node two_tier = build_two_tier();
	BTree.Node full_two_tier = build_full_two_tier();
	BTree.Node three_tier = build_thin_three_tier();
	print_tree(empty);
	print_tree(full_leaf_root);
	print_tree(two_tier);
	print_tree(full_two_tier);
	print_tree(three_tier);
	System.out.println("Invariant Check for two_tier: " + check_invariants(two_tier, true));
    }

    boolean any_false(Invariants invars) {
	boolean wrong = 
	    invars.ascending &&
	    invars.not_fat &&
	    invars.not_starving &&
	    invars.good_root &&
	    invars.height_match &&
	    invars.child_key_order;
	
	return !wrong;
    }

    boolean check_height(BTree.Node node, CheckHeight res) {
	List<Integer> depth = new ArrayList<Integer>();
	check_leaf_height(node, depth, 0);
	int val = 0;
	boolean same = false;
	for (int i=0; i < depth.size(); i++) {
	    if (i == 0) {
		val = depth.get(i);
		res.result_height = val;
		same = true;
	    } else {
		int other = depth.get(i);
		if (val != other) {
		    same = false;
		    break;
		}
	    }
	}
	return same;
    }

    boolean check_node_key_range(BTree.Node node, int low, int high, boolean recurse) {

	for (int i=0; i < node.getNumKeys(); i++) {
	    if (node.getKeys()[i] <= low || // key is out of low range
		node.getKeys()[i] >= high) {// key is out of high range
		return false;
	    }
	    if (!node.isLeaf() && recurse) {
		boolean child_result = check_node_key_range(node.getChildren()[i], 
							 low, node.getKeys()[i], recurse);
		if (!child_result) {
		    return false;
		}
	    }
	    low = node.getKeys()[i];
	}
	if (!node.isLeaf() && recurse) {
	    // need to check that last child is in range too
	    boolean child_result = check_node_key_range(node.getChildren()[node.getNumKeys()], 
						     low, high, recurse);
	    if (!child_result) {
		return false;
	    }
	}
	return true;
    }

    void check_leaf_height(BTree.Node node, List<Integer> depth, int current_depth) {
	if (node.isLeaf()) {
	    depth.add(current_depth);
	} else {
	    for (int i=0; i <= node.getNumKeys(); i++) {
		check_leaf_height(node.getChildren()[i], depth, current_depth + 1);
	    }
	}
    }
    
    class CheckHeight {
	int result_height;
    }

    Invariants check_invariants(BTree.Node node, boolean is_root) {
	Invariants invars = new Invariants();

	if (is_root && node == null) {
	    invars.ascending = true;
	    invars.not_fat = true;
	    invars.not_starving = true;
	    invars.good_root = true;
	    invars.height_match = true;
	    invars.child_key_order = true;
	} else {
	    // A node's keys are kept in ascending order, starting at index 0.
	    invars.ascending = true;
	    int prev = Integer.MIN_VALUE;
	    for (int i=0; i < node.getNumKeys(); i++) {
		if (node.getKeys()[i] <= prev) {
		    invars.ascending = false;
		    break;
		}
	    }

	    // A node may have at most m children.
	    invars.not_fat = node.getNumKeys() < BTREE_ORDER;

	    // Non-root nodes have at least round_up(m/2) - 1 keys
	    int min_keys = (int) Math.ceil(BTREE_ORDER/2.0) - 1;
	    invars.not_starving = is_root;
	    if (!is_root) {
		invars.not_starving = node.getNumKeys() >= min_keys;
	    }

	    // If the root is not a leaf, it has at least two children.
	    invars.good_root = true;
	    if (is_root && !node.isLeaf()) {
		invars.good_root = node.getNumKeys() >= 1;
	    }

	    // All leaves are at the same level. Only need to check this if you
	    // are running the invariant tests on the root of the entire tree.
	    invars.height_match = true;
	    if (is_root) {
		invars.height_match = check_height(node, new CheckHeight());
	    }
  
	    // child[i] holds keys that are less than key[i]. The final child
	    // holds keys that are larger than the final key.
	    //  child_key_order = false;
	    invars.child_key_order = true;
	    if (is_root && !node.isLeaf()) {
		invars.child_key_order = check_node_key_range(node, Integer.MIN_VALUE, 
							      Integer.MAX_VALUE, true);
	    }

	    if (any_false(invars)) {
		return invars;
	    } else if (!node.isLeaf()) {
		for (int i=0; i <= node.getNumKeys(); i++) {
		    invars = check_invariants(node.getChildren()[i], false);
		    if(any_false(invars)) {
			return invars;
		    }
		}
	    }
	}  
	return invars;
    }

    String get_label_for_dot(BTree.Node node) {
	StringBuilder buf = new StringBuilder();
	for (int i=0; i < node.getNumKeys(); i++) {
	    buf.append("" + node.getKeys()[i]);
	    if (i+1 < node.getNumKeys()) {
		buf.append(" ");
	    }
	}
	return buf.toString();
    }

    void print_dot_label(BTree.Node node) {
	System.out.println("   " + get_id_for_dot(node) + " [label=\"" +
			   get_label_for_dot(node) + "\"];\n");
    }


    void print_graphviz_dotfile(BTree.Node node, int depth) {
	String spaces = "    ";
	if (depth == 0) {
	    print_dot_label(node);
	}
	int idx = 0;
	String my_id = get_id_for_dot(node);
	for ( ; idx < node.getNumKeys(); idx++) {
	    if (!node.isLeaf()) { // don't recurse if this is a leaf.
		print_dot_label(node.getChildren()[idx]);
		System.out.println(spaces + my_id + " -- " 
				   + get_id_for_dot(node.getChildren()[idx]) + ";\n");
		print_graphviz_dotfile(node.getChildren()[idx], depth + 1);
	    }
	}
	// there is always one leftover child, assuming it is not a leaf.
	if (!node.isLeaf()) {
	    print_dot_label(node.getChildren()[idx]);
	    System.out.println(spaces + my_id + " -- " + 
			       get_id_for_dot(node.getChildren()[idx]) + ";\n");
	    print_graphviz_dotfile(node.getChildren()[idx], depth + 1);
	}
    }


    void print_tree(BTree.Node root) {
	System.out.println("graph btree {\n");
	int depth = 0;
	print_graphviz_dotfile(root, depth);
	System.out.println("}");
    }

    class Invariants {
	boolean ascending;
	boolean not_fat;
	boolean not_starving;
	boolean good_root;
	boolean height_match;
	boolean child_key_order;

	public String toString() {
	    if (ascending &&
		not_fat &&
		not_starving &&
		good_root &&
		height_match &&
		child_key_order) {
		return "Everything Checks Out!";
	    } else {
		return "Failures";
	    }
	}
    }

    boolean private_contains(BTree.Node node, int key) {
	if (node == null) {
	    return false;
	}
	for (int i=0; i < node.getNumKeys(); i++) {
	    if (node.getKeys()[i] == key) {
		return true;
	    } else if (!node.isLeaf() && node.getKeys()[i] > key) {
		// if the key is larger than target, answer will be in child i
		return private_contains(node.getChildren()[i], key);
	    }
	}
	if (!node.isLeaf() && node.getKeys()[node.getNumKeys()-1] < key) {
	    return private_contains(node.getChildren()[node.getNumKeys()], key);
	}
	return false;
    }

}
