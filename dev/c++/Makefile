CFLAGS=-Wall -DDBG_LVL=3
CXXFLAGS=$(CFLAGS)

%: %.cpp
	g++ $(CXXFLAGS) $< -o $@

debug: debug.cpp debug.h Makefile
	g++ $(CXXFLAGS) $< -o $@

clean:
	@rm -fv *.o structTest debug
