#include <stdio.h>

int fibonacci_recursive(int n) {
	if (n < 2){
		return 1;
	}else{
		return fibonacci_recursive(n-2) + fibonacci_recursive(n-1);
	}
}

int fibonacci_loop(int n) {

	int a=1,b=1,m = 1;

	while (m < n) {
		int _a = b;
		b = a + b;
		a = _a;
		m++;
	}
	
	return b;
}

int main (void) {

	int ii = 0;
	for (ii = 0; ii < 100; ii++) {
		printf("%03d: %d\t%d\n", ii, fibonacci_recursive(ii), fibonacci_loop(ii));
	}

	return 0;
}
