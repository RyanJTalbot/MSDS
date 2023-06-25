#include <iostream>

using namespace std;

int main() {
  int andy = 42;
  cout << "andy: " << andy << endl;
  cout << "&andy: " << &andy << endl;
  int* ted = &andy;
  cout << "ted: " << ted << endl;
  cout << "*ted: " << *ted << endl;
  *ted = NULL;
  cout << "made ted a null reference. what is it now?" << endl;
  cout << "ted: " << ted << endl;
  cout << "*ted: " << *ted << endl;
}
