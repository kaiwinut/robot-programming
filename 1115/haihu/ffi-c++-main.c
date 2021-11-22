#include <stdio.h>

double sinc(double x);
void hello(char *str);

int main() {
  double f = 1.0;
  hello("world");
  fprintf(stderr, "sinc(%f) = %f\n", f, sinc(f));
}
