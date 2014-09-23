#include <iostream>
#include <ostream>
#include <string>
#include "Status.h"

/* pulseWidth,dutyCycle  */ 
const Status::ledPattern Status::ledPatterns [Status::NUM_STATUSTYPES] = {
	{1000, 100 },	/* ALL_GOOD */
	{ 500, 50  },	/* POWER_FAIL */
	{ 500, 10  },	/* COMPASS_FAIL */
	{ 500, 20  }	/* GPS_FAIL */
};

Status::Status()
{
	std::cout << "allgood=" << ALL_GOOD << " pw=" << ledPatterns[ALL_GOOD].pulseWidth << "; dc=" << ledPatterns[ALL_GOOD].dutyCycle;

}

int main() {
	Status st = Status();
	return 0;
}
