# Where to find user code.
USER_DIR = .

# Flags passed to the preprocessor.
CPPFLAGS =

# Flags passed to the C++ compiler.
CXXFLAGS = -g -Wall -Wextra -Wno-write-strings2 -std=c++0x -pthread

# House-keeping build targets.

all : btree_unittest

clean :
	rm -f *.o *~ btree_unittest

# Assignment-specific build rules below.

UTFramework.o: $(USER_DIR)/UTFramework.cpp	\
                 $(USER_DIR)/UTFramework.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/UTFramework.cpp

btree_unittest.o: $(USER_DIR)/UTFramework.o $(USER_DIR)/btree_unittest.cpp btree_unittest_help.o btree.o
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/btree_unittest.cpp

btree_unittest: UTFramework.o btree_unittest.o btree_unittest_help.o btree.o
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -o btree_unittest UTFramework.o btree_unittest.o btree_unittest_help.o btree.o


%.o : %.cpp
	$(CXX) -c $(CPPFLAGS) $(CXXFLAGS) $< -o $@
