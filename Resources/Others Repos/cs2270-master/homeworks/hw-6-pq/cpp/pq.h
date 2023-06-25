#ifndef pq_h
#define pq_h

#include <string>
#include "pq_struct.h"

using namespace std;

pq* init_priority_queue();

void insert(pq* &queue, string &text, float priority);

string remove(pq* &queue);

string peek(pq* &queue);

#endif
