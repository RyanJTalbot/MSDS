/*
 * huffman_driver.cpp
 *
 * You can run this in 'manual' mode with the --manual flag. This will
 * call the manual_driver() function in huffman.cpp. That is a basic
 * stub of how you should proceed, so I recommend doing that.
 *
 * To run the unit test framework, ensure that the line that says
 * UTFrameworkInit is not commented out.
 */
#include <iostream>
#include <cmath>
#define EPSILON 0.0001
#include "UTFramework.h"
#include "huffman.h"

using namespace Thilenius;
using namespace std;

bool checkTree(freq_info*& node);
freq_info* combine(freq_info*& left, freq_info*& right);
freq_info* build_prefab_tree();
map<char, string> build_prefab_map();
bool are_same(float a, float b);

SUITE_BEGIN("Huffman")

TEST_BEGIN("HuffTreeSupernode")
{
  freq_info* childA = init_freq_info_leaf('a', 0.3);
  freq_info* childB = init_freq_info_leaf('b', 0.4);
  freq_info* parent = init_freq_info_supernode(childA, childB);
  IsTrue("Parent has sum of frequencies?",
	 are_same(parent->freq, childA->freq + childB->freq),
	 "Parent does not have sum of frequences.");
  IsTrue("Parent has child links for left and right?",
	 parent->left == childA &&
	 parent->right == childB,
	 "Child nodes are wrong.");
  IsTrue("Is parent marked as leaf?",
	 !parent->is_leaf,
	 "Parent should not be a leaf.");
  
}TEST_END

TEST_BEGIN("HuffTree")
{
  tree_queue queue = read_corpus("pkd.txt");
  freq_info* tree = build_huffman_tree(queue);
  bool result = checkTree(tree);
  IsTrue("Tree Validity", result, "Huffman Tree not valid");
}TEST_END

TEST_BEGIN("HuffTable")
{
  freq_info* root = build_prefab_tree();
  IsTrue("Sanity Check of Prefab Tree",
	 root->freq == 36.0,
	 "Bzzt");
  
  map<char, string> table = build_encoding_map(root);
  IsTrue("Correct Symbol Count",
	 table.size() == 16,
	 "Wrong number of symbols in map.");
  // spot check some values
  string exp;
  exp = "...";
  IsTrue("Spot Check", table['e'] == exp, "Wrong bitstring");
  exp = ".^^.";
  IsTrue("Spot Check", table['t'] == exp, "Wrong bitstring");
  exp = "^^..^";
  IsTrue("Spot Check", table['l'] == exp, "Wrong bitstring");
  
}TEST_END

TEST_BEGIN("Encode")
{
  map<char, string> table = build_prefab_map();
  // ret['a'] = ".^.";
  // ret['m'] = ".^^^";
  // ret['t'] = ".^^.";
  IsTrue("Sanity Check of Prefab Map",
	 table['a'] == ".^.",
	 "Bzzt");
  string in = "aammttamt";
  string result = encode(in, table);
  string exp = ".^..^..^^^.^^^.^^..^^..^..^^^.^^.";
  IsTrue("Check Result", result == exp, "Result not exactly correct");
}TEST_END

TEST_BEGIN("Decode")
{
  freq_info* tree = build_prefab_tree();
  string in = ".^..^..^^^.^^^.^^..^^..^..^^^.^^.";  
  string result = decode(in, tree);
  string exp = "aammttamt";
  IsTrue("Check Result", result == exp, "Result not entirely accurate");

}TEST_END

TEST_BEGIN("AllInSequence")
{
  tree_queue queue = read_corpus("pkd.txt");
  freq_info* huffman_root = build_huffman_tree(queue);
  map<char, string> encoding_map = build_encoding_map(huffman_root);
  
  string short_orig = "BREWED ON THE BANKS OF THE MIGHTY ST. VRAIN";
  string medium_orig = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.";

  string long_orig = "Four score and seven years ago our fathers brought forth on this continent a new nation, conceived in liberty, and dedicated to the propostion that all men are created equal. Now we are engaged in a great civil war, testing whether that nation, or any nation, so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this. But, in a larger sense, we can not dedicate, we can not consecrate, we can not hallow this ground. The brave men, living and dead, who struggled here, have consecrated it, far above our poor power to add or detract. The world will little note, nor long remember what we say here, but it can never forget what they did here. It is for us the living, rather, to be dedicated here to the unfinished work which they who fought here have thus far so nobly advanced. It is rather for us to be here dedicated to the great task remaining before us---that from these honored dead we take increased devotion to that cause for which they gave the last full measure of devotion---that we here highly resolve that these dead shall not have died in vain: that this nation, under God, shall have a new birth of freedom: and that government of the people, by the people, for the people, shall not perish from the earth."; 

  string short_enc = encode(short_orig, encoding_map);
  string short_rebuilt = decode(short_enc, huffman_root);
  IsTrue("Short String", short_rebuilt == short_orig, "Short didn't make it");

  string med_enc = encode(medium_orig, encoding_map);
  string med_rebuilt = decode(med_enc, huffman_root);
  IsTrue("Medium String", med_rebuilt == medium_orig, "Medium didn't make it");

  string long_enc = encode(long_orig, encoding_map);
  string long_rebuilt = decode(long_enc, huffman_root);
  IsTrue("Long String", long_rebuilt == long_orig, "Long didn't make it");

}TEST_END

SUITE_END

int main (int argc, char* argv[])
{
  if (argc == 2 && string(argv[1]) == string("--manual")) {
    manual_driver();
  } else {
    cout << "Read the comment at the top of huffman_driver.cpp "
	 << "to see how to run this thing." << endl;
    UTFrameworkInit;
  }
}

bool checkTree(freq_info*& node) {
  if (node == NULL) {
    IsTrue("Fail", false, "Found null node in tree.");
    return false;
  }
  if (!node->is_leaf) {
    if (node->left == NULL || node->right==NULL) {
      IsTrue("Fail", false, "Found null child node in internal node.");
      return false;
    }
    float sum = node->left->freq + node->right->freq;
    if (sum != node->freq) {
      IsTrue("Fail", false, "Found parent node freq that is not sum of child frequencies.");
      return false;
    }
    checkTree(node->left);
    checkTree(node->right);
  }
  return true;
}

freq_info* combine(freq_info*& left, freq_info*& right) {
  freq_info* parent = new freq_info;
  parent->freq = left->freq + right->freq;
  parent->left = left;
  parent->right = right;
  parent->is_leaf = false;
  return parent;
}

freq_info* build_prefab_tree() {
  freq_info* e = init_freq_info_leaf('e', 4.0);     // 1
  freq_info* a = init_freq_info_leaf('a', 4.0);     // 2
  freq_info* space = init_freq_info_leaf(' ', 7.0); // 3
  freq_info* n = init_freq_info_leaf('n', 2.0);     // 4
  freq_info* t = init_freq_info_leaf('t', 2.0);     // 5
  freq_info* m = init_freq_info_leaf('m', 2.0);     // 6
  freq_info* i = init_freq_info_leaf('i', 2.0);     // 7
  freq_info* h = init_freq_info_leaf('h', 2.0);     // 8
  freq_info* s = init_freq_info_leaf('s', 2.0);     // 9
  freq_info* f = init_freq_info_leaf('f', 3.0);     // 10
  freq_info* o = init_freq_info_leaf('o', 1.0);     // 11
  freq_info* u = init_freq_info_leaf('u', 1.0);     // 12
  freq_info* x = init_freq_info_leaf('x', 1.0);     // 13
  freq_info* p = init_freq_info_leaf('p', 1.0);     // 14
  freq_info* r = init_freq_info_leaf('r', 1.0);     // 15
  freq_info* l = init_freq_info_leaf('l', 1.0);     // 16
  
  freq_info* ou = combine(o, u);
  freq_info* xp = combine(x, p);
  freq_info* rl = combine(r, l);
  freq_info* nou = combine(n, ou);
  freq_info* ixp = combine(i, xp);
  freq_info* rlf = combine(rl, f);
  freq_info* tm = combine(t, m);
  freq_info* hs = combine(h, s);
  freq_info* enou = combine(e, nou);
  freq_info* atm = combine(a, tm);
  freq_info* ixphs = combine(ixp, hs);
  freq_info* rlf_space= combine(rlf, space);
  freq_info* enouatm= combine(enou, atm);
  freq_info* ixphsrlf_space= combine(ixphs, rlf_space);
  freq_info* root = combine(enouatm, ixphsrlf_space);
  return root;
}

map<char, string> build_prefab_map() {
  map<char, string> ret;
  ret['a'] = ".^.";
  ret['m'] = ".^^^";
  ret['t'] = ".^^.";
  return ret;
}

bool are_same(float a, float b) {
    return fabs(a - b) < EPSILON;
}
