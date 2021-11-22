// ffi-c++.cpp
#include <iostream>
#include <math.h>

int  f (int)  { return 0; }
int  f (void) { return 1; }
void g (void) { int i = f(), j = f(0); }

extern "C" {
  double sinc(double d) {
    return(sin(d)/d);
  }
  void hello(char* str) {
    std::cout << "hello " << str << std::endl;
  }
}

