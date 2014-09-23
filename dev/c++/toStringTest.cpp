#include <iostream>
#include <ostream>
#include <string>

#include "toStringTest.h"

std::string Person::toString() {
	return "blah";
}


int main()
{
	int anInt = -20;
	unsigned int anUnsignedInt = -19;
	unsigned int anotherUnsignedInt = 19;
	int aConvert;
	aConvert = (int) anUnsignedInt;

	Person p("John", "Doe");
	std::cout << p << '\n';
	std::cout << p.toString() << -10 << "|" << anInt << "|" << anotherUnsignedInt << "|" << anUnsignedInt << "|" << aConvert << '\n';

	return 0;
}
