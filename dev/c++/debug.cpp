#include <iostream>
#include <fstream>

using namespace std;

#include "debug.h"

int main (int argc, char **argv) {

	cout << "hi...\n";
	out("this is an out statement! %d\n", 10);
	cout << "hefe" << endl;
	dbg(2,"this is a level 2 debug %s, %.2f\n", "message", -123.342);
	dbg(3,"this is a level 3 debug %s, %.2f\n", "message", -123.342);

	return 0;
}
