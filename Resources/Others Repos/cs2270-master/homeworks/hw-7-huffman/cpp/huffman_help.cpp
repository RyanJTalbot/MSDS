/*
 * huffman_help.cpp
 *
 * Don't edit this file. It contains already-implemented versions of
 * several functions defined in huffman.h. Retrograde will use its own
 * version of this.
 */

#include <iostream>
#include <fstream>
#include <map>
#include <queue>
#include <algorithm>
#include <string>
#include <cctype>
#include "huffman.h"

using namespace std;

freq_info* init_freq_info_leaf(char symbol, float freq) {
  // this is already done, and you shouldn't need to modify it.
  freq_info* ret = new freq_info;
  ret->symbol = symbol;
  ret->freq = freq;
  ret->left = NULL;
  ret->right = NULL;
  ret->is_leaf = true;
  return ret;
}

void add_freq(char c, map<char, int> &data) {
  // already done for you. This is a helper function of 'read_corpus'.
  if (data[c] == 0) {
    data[c] = 1;
  } else {
    data[c] = data[c] + 1;
  }
}

tree_queue read_corpus(string filename) {
  // already done for you. This reads the contents of a file and
  // produces a priority queue with leaf nodes.
  ifstream myfile;
  string line;
  tree_queue queue;
  myfile.open(filename.c_str());
  map<char, int> freq;
  if (myfile.is_open()) {
    while (myfile.good()) {
      getline(myfile, line);
      for (unsigned i=0; i < line.length(); i++) {
	add_freq(line[i], freq);
      }
      add_freq('\n', freq);
    }
    myfile.close();
    int largest = 0;
    int sum = 0;
    for (map<char, int>::iterator it = freq.begin();
	 it != freq.end(); it++) {
      largest = max(largest, it->second);
      sum = sum + it->second;
    }
    //    cout << "Number of unique characters: " << freq.size() << endl;
    //    cout << "Number of character instances: " << sum << endl;
    //    cout << "Most frequent char was seen " << largest << " times." << endl;

    // now we know the total number so we can calculate frequency data.
    float fsum = (float) sum;
    for (map<char, int>::iterator it = freq.begin();
	 it != freq.end(); it++) {
      freq_info* info = init_freq_info_leaf(it->first, it->second);

      info->symbol = it->first;
      info->freq = (float) it->second / fsum;
      queue.push(info);
    }
    //    cout << "Read file: " << filename << endl;
  } else {
    cout << "WARNING: could not read file: " << filename << endl;
  }
  return queue;
}

/**
 * You might find the following function informative to use once you
 * have the required functions working. I will leave this here for you
 * to use, or not.
 **/
void do_encoding_test(string& original_string, map<char, string>& encoding_map, 
		      freq_info*& huffman_root) {
  string reconstituted_string;
  string encoded_string;
  int original_bits; // 8 bits * byte_size_of_char * string_length
  int encoded_bits; // string_length
  float compression_ratio; // encoded / original
  bool are_same;

  cout << "\n------------ Encode / Decode Test --------------" << endl;
  original_bits = 8 * sizeof(char) * original_string.size();
  cout << "Original size: " << original_bits << endl;
  encoded_string = encode(original_string, encoding_map);
  encoded_bits = encoded_string.size();
  compression_ratio = (float) encoded_bits / (float) original_bits;
  cout << "Encoded size: " << encoded_bits << endl;
  cout << "Compression ratio: " << compression_ratio << endl;
  reconstituted_string = decode(encoded_string, huffman_root);
  are_same = reconstituted_string == original_string;
  cout << "Are strings the same? " << are_same << endl; 
}
