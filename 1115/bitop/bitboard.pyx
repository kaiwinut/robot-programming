cdef extern unsigned long long getBit (unsigned long long, int)
cdef extern unsigned long long setBit (unsigned long long, int)
cdef extern unsigned long long popBit (unsigned long long, int)
cdef extern void showBB (unsigned long long)

def getBit_py(n1, n2):
	cdef unsigned long long bb = n1
	cdef int n = n2
	return getBit(bb, n)

def setBit_py(n1, n2):
	cdef unsigned long long bb = n1
	cdef int n = n2
	return setBit(bb, n)

def popBit_py(n1, n2):
	cdef unsigned long long bb = n1
	cdef int n = n2
	return popBit(bb, n)

def showBB_py(n1):
	cdef unsigned long long bb = n1
	return showBB(bb)

# #include <stdio.h>

# unsigned long long getBit(unsigned long long bb, int n) { return bb & (1ull << n); }
# unsigned long long setBit(unsigned long long bb, int n) { return bb | (1ull << n); }
# unsigned long long popBit(unsigned long long bb, int n) { return bb & ~(1ull << n); }
# void showBB(unsigned long long bb)
# {
# 	printf("Board: %lld", bb);
# 	for (int i = 0; i < 64; i ++)
# 	{
# 		if (i % 8 == 0) printf("\n");
# 		if (getBit(bb, i)) printf("1 ");
# 		else printf(". ");
# 	}
# 	printf("\n\n");
# }

# // int main()
# // {
# // 	unsigned long long bb;
# // 	bb = setBit(bb, 5);
# // 	bb = setBit(bb, 10);
# // 	bb = setBit(bb, 15);
# // 	bb = popBit(bb, 10);
# // 	showBB(bb);

# // 	return 0;	
# // }