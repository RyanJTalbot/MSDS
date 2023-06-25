#include "UTFramework.h"
#include "btree_unittest_help.h"

using namespace Thilenius;

vector<int> get_random_data(int how_many, int upper_bound);

bool passed_remove4 = false;

SUITE_BEGIN("BTree")

TEST_BEGIN("Contains")
{
  btree* root_empty = build_empty();
  btree* root_full_leaf = build_full_leaf_root(); // 10, 20, 30, 40
  btree* root_two_tier = build_two_tier(); // 5 8 10 13 15 17 19 20 23 27 30 33 35 38
  IsTrue("Contains", !contains(root_empty, 42), "Empty tree shouldn't have anything");
  IsTrue("Contains", contains(root_full_leaf, 10), "Key not found");
  IsTrue("Contains", contains(root_full_leaf, 20), "Key not found");
  IsTrue("Contains", !contains(root_full_leaf, 15), "Key should not be found");
  IsTrue("Contains", !contains(root_full_leaf, 100), "Key should not be found");

  IsTrue("Contains", !contains(root_two_tier, 18), "Key should not be found");
  IsTrue("Contains", !contains(root_two_tier, 39), "Key should not be found");
  IsTrue("Contains", contains(root_two_tier, 20), "Key not found");
  IsTrue("Contains", contains(root_two_tier, 5), "Key not found");
  IsTrue("Contains", contains(root_two_tier, 17), "Key not found");
  IsTrue("Contains", contains(root_two_tier, 38), "Key not found");
  
}TEST_END

TEST_BEGIN("Insert1")
{
  // The tree starts with an empty (non-null) root. We will insert
  // into it four times and expect the keys to be present and in the
  // right spot. The node size of the tree should remain constant; the
  // key size should grow by one each time.
  btree* root = build_empty();
  int nnodes = 0;
  int nkeys = 0;
  invariants* invar = new invariants;
  check_invariants(invar, root, true);
  IsTrue("Check Empty", !any_false(invar), "Default Empty Tree Breaks Invariant");
  check_size(root, nnodes, nkeys, true);
  IsTrue("Check Node Count", nnodes == 1, "Should have one node only");
  IsTrue("Check Key Count", nkeys == 0, "Wrong number of keys");

  insert(root, 10);
  check_size(root, nnodes, nkeys, true);
  IsTrue("Check Node Count", nnodes == 1, "Should have one node only");
  IsTrue("Check Key Count", nkeys == 1, "Wrong number of keys");
  check_invariants(invar, root, true);
  IsTrue("Check Invariants", !any_false(invar), "Inserting Breaks Invariant");
  IsTrue("Look for known values", private_contains(root, 10), "Tree must contain 10");  

  insert(root, 40);
  check_invariants(invar, root, true);
  check_size(root, nnodes, nkeys, true);
  IsTrue("Check Node Count", nnodes == 1, "Should have one node only");
  IsTrue("Check Key Count", nkeys == 2, "Wrong number of keys");
  IsTrue("Check Invariants", !any_false(invar), "Inserting Breaks Invariant");
  IsTrue("Look for known values", private_contains(root, 40), "Tree must contain 40");  

  insert(root, 30);
  check_size(root, nnodes, nkeys, true);
  IsTrue("Check Node Count", nnodes == 1, "Should have one node only");
  IsTrue("Check Key Count", nkeys == 3, "Wrong number of keys");
  check_invariants(invar, root, true);
  IsTrue("Check Invariants", !any_false(invar), "Inserting Breaks Invariant");
  IsTrue("Look for known values", private_contains(root, 30), "Tree must contain 30");  

  insert(root, 20);
  check_size(root, nnodes, nkeys, true);
  IsTrue("Check Node Count", nnodes == 1, "Should have one node only");
  IsTrue("Check Key Count", nkeys == 4, "Wrong number of keys");
  check_invariants(invar, root, true);
  IsTrue("Check Invariants", !any_false(invar), "Inserting Breaks Invariant");
  IsTrue("Look for known values", private_contains(root, 20), "Tree must contain 20");  
}TEST_END

TEST_BEGIN("Insert2")
{
  
  btree* root = build_full_leaf_root();
  int nnodes = 0;
  int nkeys = 0;
  invariants* invar = new invariants;
  check_invariants(invar, root, true);
  IsTrue("Check Empty", !any_false(invar), "Default Full Leaf Root Breaks Invariant");
  check_size(root, nnodes, nkeys, true);
  IsTrue("Check Node Count", nnodes == 1, "Should have one node only");
  IsTrue("Check Key Count", nkeys == 4, "Wrong number of keys");

  insert(root, 38);
  check_size(root, nnodes, nkeys, true);
  IsTrue("Check Node Count", nnodes == 3, "Should have three nodes now");
  IsTrue("Check Key Count", nkeys == 5, "Wrong number of keys");
  check_invariants(invar, root, true);
  IsTrue("Check Invariants", !any_false(invar), "Inserting Breaks Invariant");
  IsTrue("Look for known values", private_contains(root, 38), "Tree must contain just-added key");

  root = build_full_leaf_root();
  insert(root, 25);
  check_size(root, nnodes, nkeys, true);
  IsTrue("Check Node Count", nnodes == 3, "Should have three nodes now");
  IsTrue("Check Key Count", nkeys == 5, "Wrong number of keys");
  check_invariants(invar, root, true);
  IsTrue("Check Invariants", !any_false(invar), "Inserting Breaks Invariant");
  IsTrue("Look for known values", private_contains(root, 25), "Tree must contain just-added key");

  root = build_full_leaf_root();
  insert(root, 5);
  check_size(root, nnodes, nkeys, true);
  IsTrue("Check Node Count", nnodes == 3, "Should have three nodes now");
  IsTrue("Check Key Count", nkeys == 5, "Wrong number of keys");
  check_invariants(invar, root, true);
  IsTrue("Check Invariants", !any_false(invar), "Inserting Breaks Invariant");
  IsTrue("Look for known values", private_contains(root, 5), "Tree must contain just-added key");

  // IsTrue("AssertionName", true, "Error Message");
}TEST_END

TEST_BEGIN("Insert3")
{
  btree* root = build_two_tier();
  int nnodes = 0;
  int nkeys = 0;
  invariants* invar = new invariants;
  check_invariants(invar, root, true);
  IsTrue("Two-Tier Tree Sanity Check", !any_false(invar), "Initial Tree Incorrect");
  check_size(root, nnodes, nkeys, true);
  int nkeys_before = nkeys;
  insert(root, 16);
  check_size(root, nnodes, nkeys, true);
  IsTrue("Check Key Count", nkeys == nkeys_before + 1, "Wrong number of keys");
  check_invariants(invar, root, true);
  IsTrue("Insertion Invariant Check", !any_false(invar), "Inserting Key Breaks Invariant(s)");

  bool ok = private_contains(root, 16);
  IsTrue("Contains Check", ok, "Tree does not contain key just inserted");
}TEST_END

TEST_BEGIN("Insert4")
{
  btree* root = build_full_two_tier();
  invariants* invar = new invariants;
  check_invariants(invar, root, true);
  IsTrue("Two-Tier Tree Sanity Check", !any_false(invar), "Initial Tree Incorrect");
  int height_before = 0;
  check_height(root, height_before);
  insert(root, 19);
  check_invariants(invar, root, true);
  IsTrue("Insertion Invariant Check", !any_false(invar), "Inserting Key Breaks Invariant(s)");
  IsTrue("Contains Check", private_contains(root, 19), "Tree does not contain key just inserted");
  int height_after = 0;
  check_height(root, height_after);
  IsTrue("Height Changed?", height_before + 1 == height_after, "Tree did not grow height by one.");
}TEST_END

TEST_BEGIN("Remove1")
{
  btree* root = build_full_leaf_root();
  int nnodes = 0;
  int nkeys = 0;
  invariants* invar = new invariants;
  check_invariants(invar, root, true);
  IsTrue("Check Empty", !any_false(invar), "Default Full Leaf Root Breaks Invariant");
  check_size(root, nnodes, nkeys, true);
  int nkeys_before = nkeys;

  remove(root, 20);
  check_size(root, nnodes, nkeys, true);
  IsTrue("Check Key Count", nkeys == nkeys_before - 1, "Wrong number of keys");
  nkeys_before = nkeys;
  check_invariants(invar, root, true);
  IsTrue("Invariant Check", !any_false(invar), "Invariants Broken");
  bool ok = !private_contains(root, 20);
  IsTrue("Contains Check", ok, "Tree still contains key that was just removed");

  remove(root, 10);
  check_size(root, nnodes, nkeys, true);
  IsTrue("Check Key Count", nkeys == nkeys_before - 1, "Wrong number of keys");
  nkeys_before = nkeys;
  check_invariants(invar, root, true);
  IsTrue("Invariant Check", !any_false(invar), "Invariants Broken");
  ok = !private_contains(root, 10);
  IsTrue("Contains Check", ok, "Tree still contains key that was just removed");

  remove(root, 40);
  check_size(root, nnodes, nkeys, true);
  IsTrue("Check Key Count", nkeys == nkeys_before - 1, "Wrong number of keys");
  nkeys_before = nkeys;
  check_invariants(invar, root, true);
  IsTrue("Invariant Check", !any_false(invar), "Invariants Broken");
  ok = !private_contains(root, 40);
  IsTrue("Contains Check", ok, "Tree still contains key that was just removed");

  remove(root, 30);
  check_size(root, nnodes, nkeys, true);
  IsTrue("Check Key Count", nkeys == nkeys_before - 1, "Wrong number of keys");
  nkeys_before = nkeys;
  check_invariants(invar, root, true);
  IsTrue("Invariant Check", !any_false(invar), "Invariants Broken");
  ok = !private_contains(root, 30);
  IsTrue("Contains Check", ok, "Tree still contains key that was just removed");
}TEST_END

TEST_BEGIN("Remove2")
{
  btree* root = build_two_tier();
  invariants* invar = new invariants;
  check_invariants(invar, root, true);
  IsTrue("Two-Tier Tree Sanity Check", !any_false(invar), "Initial Tree Incorrect");
  remove(root, 17);
  check_invariants(invar, root, true);
  IsTrue("Insertion Invariant Check", !any_false(invar), "Inserting Key Breaks Invariant(s)");
  bool ok = !private_contains(root, 17);
  IsTrue("Contains Check", ok, "Tree still contains key that was just removed");
}TEST_END


TEST_BEGIN("Remove3")
{
  btree* root = build_full_two_tier();
  invariants* invar = new invariants;
  check_invariants(invar, root, true);
  IsTrue("Two-Tier Tree Sanity Check", !any_false(invar), "Initial Tree Incorrect");
  int height_before = 0;
  check_height(root, height_before);
  remove(root, 6);
  check_invariants(invar, root, true);
  IsTrue("Invariant Check", !any_false(invar), "Remove Breaks An Invariant");
  bool ok = !private_contains(root, 6);
  IsTrue("Contains Check", ok, "Tree still contains key that was just removed");
  int height_after = 0;
  check_height(root, height_after);
  IsTrue("Height Same?", height_before == height_after , "Height should not have changed");
}TEST_END


TEST_BEGIN("Remove4")
{
  btree* root = build_thin_three_tier();
  invariants* invar = new invariants;
  check_invariants(invar, root, true);
  IsTrue("Three-Tier Tree Sanity Check", !any_false(invar), "Initial Tree Incorrect");
  int height_before = 0;
  check_height(root, height_before);
  remove(root, 5);
  check_invariants(invar, root, true);
  IsTrue("Invariant Check", !any_false(invar), "Remove Breaks An Invariant");
  passed_remove4 = !any_false(invar);
  bool ok = !private_contains(root, 5);
  IsTrue("Contains Check", ok, "Tree still contains key that was just removed");
  passed_remove4 = passed_remove4 && ok;
  int height_after = 0;
  check_height(root, height_after);
  bool height_reduced = height_before == height_after + 1;
  IsTrue("Height Same?", height_reduced, "Height should reduce by one");
  passed_remove4 = passed_remove4 && height_reduced;
}TEST_END


TEST_BEGIN("BulkRandom")
{
  if (passed_remove4) {
    vector<int> data = get_random_data(400, 1000);
    btree* root = build_empty();
    invariants* invar = new invariants;
    for (size_t i=0; i < data.size(); i++) {
      insert(root, data[i]);
      if (i % 10 == 0) {
	check_invariants(invar, root, true);
	IsTrue("Invariant Check", !any_false(invar), "Invariant Broken During Bulk Insert");
	bool ok = contains(root, data[i]);
	IsTrue("Check Inserted Key", ok, "Inserted key not present");
	if (any_false(invar) || !ok) {
	  break;
	}
      }
    }
    for (size_t i=0; i < data.size(); i++) {
      remove(root, data[i]);
      if (i % 10 == 0) {
	check_invariants(invar, root, true);
	IsTrue("Invariant Check", !any_false(invar), "Invariant Broken During Bulk Remove");
	bool ok = !contains(root, data[i]);
	IsTrue("Check Removed Key", ok, "Removed key is present");
	if (any_false(invar) || !ok) {
	  break;
	}
      }
    }
  } else {
    IsTrue("Need To Pass Remove4", false, "Pass Remove4 To Unlock The Secret Level");
  }

}TEST_END

SUITE_END

vector<int> get_random_data(int how_many, int upper_bound) {
  vector<int> numbers;
  for (int i=0; i < how_many; i++) {
    int r = rand() % upper_bound;
    numbers.push_back(r);
  }
  return numbers;
}

void print_trees() {
  int nnodes = 0;
  int nkeys = 0;

  cout << "Tree 'empty' used in tests Insert1 and BulkRandom" << endl << endl;
  btree* root = build_empty();
  check_size(root, nnodes, nkeys, true);  
  cout << nnodes << " nodes, " << nkeys << " keys." << endl;
  print_tree(root);
  cout << endl;

  cout << "Tree 'full_leaf_root' used in tests Insert2 and Remove1 " << endl << endl;
  root = build_full_leaf_root();
  check_size(root, nnodes, nkeys, true);  
  cout << nnodes << " nodes, " << nkeys << " keys." << endl;
  print_tree(root);
  cout << endl;

  cout << "Tree 'two_tier' used in tests Insert3 and Remove2 " << endl << endl;
  root = build_two_tier();
  check_size(root, nnodes, nkeys, true);  
  cout << nnodes << " nodes, " << nkeys << " keys." << endl;
  print_tree(root);
  cout << endl;

  cout << "Tree 'full_two_tier' used in tests Insert4 and Remove3" << endl << endl;
  root = build_full_two_tier();
  check_size(root, nnodes, nkeys, true);  
  cout << nnodes << " nodes, " << nkeys << " keys." << endl;
  print_tree(root);
  cout << endl;

  cout << "Tree 'thin_three_tier' used in test Remove4" << endl << endl;
  root = build_thin_three_tier();
  check_size(root, nnodes, nkeys, true);  
  cout << nnodes << " nodes, " << nkeys << " keys." << endl;
  print_tree(root);
  cout << endl;

}

int main (int argc, char* argv[]) {	
  if (argc == 2 && strcmp(argv[1], "--print-trees") == 0) {
    print_trees();
    return 0;
  } else {
    UTFrameworkInit;
  }
  
}
