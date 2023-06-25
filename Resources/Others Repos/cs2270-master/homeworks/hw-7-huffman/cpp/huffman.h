/*
 * huffman.h
 *
 * Header file for a struct and several functions prototypes.
 *
 * Some functions are already implemented for you in the cpp
 * file. Others are optional. The required ones are grouped.
 */
#ifndef huffman_h
#define huffman_h

#include <vector>
#include <string>
#include <queue>
#include <map>

using namespace std;

#define LEFT_CHAR '.'
#define RIGHT_CHAR '^'

/* ------------------------------------------------------- Done for you ---- */
struct freq_info {
  char symbol;
  float freq;
  freq_info* left;
  freq_info* right;
  bool is_leaf;
  bool operator() (freq_info* a, freq_info* b) {
    return a->freq > b->freq;
  }
};


// I got sick of typing all this template parameterization stuff. So I
// typedef'ed the priority queue type to simply 'tree_queue'.
typedef priority_queue<freq_info*, vector<freq_info*>, freq_info> tree_queue;

void manual_driver();

freq_info* init_freq_info_leaf(char symbol, float freq);

void add_freq(char c, map<char, int> &data);

tree_queue read_corpus(string filename);

void do_encoding_test(string& original_string, map<char, string>& encoding_map, 
		      freq_info*& huffman_root);

/* ----------------------------------------------------------- Optional ---- */

void debug_queue(tree_queue &queue);

void debug_tree(freq_info*& node, int& level);

void debug_encoding_map(map<char, string>& huffman_map);

/* -------------------------------------- Required for you to implement ---- */

freq_info* init_freq_info_supernode(freq_info* left, freq_info* right);

freq_info* build_huffman_tree(tree_queue &queue);

map<char, string> build_encoding_map(freq_info*& huffman_root);

string encode(string& original, map<char, string>& encoding_map);

string decode(string& encoded, freq_info*& huffman_root);

#endif
