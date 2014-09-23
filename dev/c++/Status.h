#ifndef Status_h
#define Status_h

class Status {
	public:
		enum statusType {
			ALL_GOOD,
			POWER_FAIL,
			COMPASS_FAIL,
			GPS_FAIL,
			NUM_STATUSTYPES
		};
		Status();

	private:
		struct ledPattern {
			unsigned long pulseWidth;
			unsigned long dutyCycle;
		};

		static const ledPattern ledPatterns [];
		
};

#endif
