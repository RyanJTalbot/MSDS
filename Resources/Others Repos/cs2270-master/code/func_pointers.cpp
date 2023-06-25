#include<iostream>
#include<string>

using namespace std;

int first_thing() {
  cout << "First thing!" << endl;
  return 10;
}

int second_thing() {
  cout << "Second thing!" << endl;
  return 20;
}

void does_nothing() {
  cout << "I am doing nothing." << endl;
}

string add_numbers_and_say_hi(int one, int two, int& result) {
  result = one + two;
  return "Hi!";
}

int get_larger(int a, int b) {
  if (a > b) {
    return a;
  }
  return b;
}

int get_smaller(int a, int b) {
  if (a < b) {
    return a;
  }
  return b;
}

int compare_with_func_pointer(int a, int b, int (*comparator) (int, int)) {
  return comparator(a, b);
}

int main() {
  cout << "Hello!" << endl;
  int (*func) () = first_thing;
  func();
  func = second_thing;
  func();
  void (*nada) () = does_nothing;
  nada();
  string (*silly_string) (int, int, int&) = add_numbers_and_say_hi;
  int sum = 0;
  string reply = silly_string(8, 13, sum);
  cout << "The silly string replied with " << reply << " and gives sum: " << sum << endl;

  // the general format for creating a function pointer is mostly
  // clear. There's just a lot of punctuation, so you need to read it
  // slowly.
  //
  // Say we want to do something that involves sorting numbers, but at
  // runtime we might want to sort either in non-ascending or
  // non-descending order, as we would in a priority queue.
  //
  // We have those two functions defined above: get_larger and
  // get_smaller. They both take two integers and return an integer.
  //
  // The format to declare and assign a pointer to a function with
  // that signature is like this:
  //
  // int (*whatever) (int, int) = the_function_name;
  //  a      b         c    d            e
  //
  // Here's what all these parts are:
  //
  // a: the return type of the function.
  // b: the name of our pointer to the function.
  // c, d: a parenthetic comma-separated list of types the function
  //       accepts as input parameters.
  // e: the name of the function we point to. Note that we OMIT the
  // parens after the function name.
  //
  int (*whatever) (int, int) = get_smaller;
  
  // Then you can call the function as whatever(int, int) and it
  // returns an int:
  int small = whatever(50, 3);
  cout << "The smaller of 50, 3 is: " << small << endl;

  // you can re-use the 'whatever' variable, as it has been declared.
  whatever = get_larger;
  int large = whatever(50, 3);
  cout << "The larger of 50, 3 is: " << large << endl;

  // we can pass function pointers like normal parameters (because
  // they *are* normal parameters, they are just of a weird type you
  // don't usually see).
  cout << "Now lets compare 20 and 30 with larger then smaller func pointers." << endl;
  large = compare_with_func_pointer(30, 20, get_larger);
  cout << "(1) Using a function pointer as a param, we get: " << large << endl;
  small = compare_with_func_pointer(30, 20, get_smaller);
  cout << "(2) Using a function pointer as a param, we get: " << small << endl;
  
  return 0;
}
