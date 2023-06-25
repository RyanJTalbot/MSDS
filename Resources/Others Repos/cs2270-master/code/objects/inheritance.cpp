#import<iostream>
#import<string>

using namespace std;

class Shape {
public:
  Shape();
};

class Ellipse : Shape {
protected:
  int x, y, r_horiz, r_vert;
public:
  Ellipse(int x, int y, int rh, int rv);
}

class Circle : Ellipse {
protected:
  int x, y, r;
public:
  Circle(int x, int y, int r);
  ~Circle();
};

Shape::Shape() {
  cout << "Shape() constructor called on " << this << endl;
}

Ellipse::Ellipse(int x, int y, int rh, int rv) {
  this->x = x;
  this->y = y;
  this->r_horiz = rh;
  this->r_vert = rv;
  cout << "Ellipse() constructor called on " << this << endl;
}

Circle::Circle(int x, int y, int r) {
  this->x = x;
  this->y = y;
  this->r = r;
  cout << "Circle() constructor called on " << this << endl;
}

Circle::~Circle() {
  cout << "Circle() deconstructor called on " << this << endl;  
}

int main() {
  cout << "Making stack-based Shape." << endl;
  Shape v;
  cout << "Now making a dynamic Shape using \"new Shape;\"" << endl;
  Shape* dv = new Shape;
  cout << "Now making a dynamic Shape using \"new Shape();\"" << endl;
  Shape *dv_init = new Shape();
  cout << "Making stack-based Circle." << endl;
  Circle mc(40, 60, 10);
}
