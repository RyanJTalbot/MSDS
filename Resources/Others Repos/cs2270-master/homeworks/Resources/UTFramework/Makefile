# Where to find user code.
USER_DIR = .

# Flags passed to the preprocessor.
CPPFLAGS =

# Flags passed to the C++ compiler.
CXXFLAGS = -g -Wall -Wextra -Wno-write-strings2 -std=c++0x -pthread

# House-keeping build targets.

all : Main

clean :
	rm -f *.o *~ Main

# Assignment-specific build rules below.

UTFramework.o: $(USER_DIR)/UTFramework.cpp	\
                 $(USER_DIR)/UTFramework.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/UTFramework.cpp

Main.o: $(USER_DIR)/Main.o $(USER_DIR)/UTFramework.o $(USER_DIR)/Main.cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/Main.cpp

Main: UTFramework.o Main.o
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -o Main UTFramework.o Main.o
