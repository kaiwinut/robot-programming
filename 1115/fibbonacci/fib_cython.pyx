cdef extern int fib (int)

def fib_py(n):
	cdef int num = n
	return fib(num)

# #include <stdio.h>

# int fib(int n)
# {
#   if (n == 0) return 0;
#   return fib(n - 1) + fib(n - 2);
# }