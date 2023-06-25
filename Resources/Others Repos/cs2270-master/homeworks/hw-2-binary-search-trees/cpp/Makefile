# Where to find user code.
USER_DIR = .

# Flags passed to the preprocessor.
CPPFLAGS =

# Flags passed to the C++ compiler.
CXXFLAGS = -g -Wall -Wextra -Wno-write-strings2 -std=c++0x

# House-keeping build targets.

all : binary_search_tree_driver

clean :
	rm -f *.o *~ binary_search_tree_driver

# Assignment-specific build rules below.

binary_search_tree.o : $(USER_DIR)/binary_search_tree.cpp	\
                 $(USER_DIR)/binary_search_tree.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/binary_search_tree.cpp

UTFramework.o: $(USER_DIR)/UTFramework.cpp	\
                 $(USER_DIR)/UTFramework.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/UTFramework.cpp

binary_search_tree_driver.o: $(USER_DIR)/binary_search_tree.o $(USER_DIR)/UTFramework.o $(USER_DIR)/binary_search_tree_driver.cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/binary_search_tree_driver.cpp

binary_search_tree_driver: UTFramework.o binary_search_tree.o binary_search_tree_driver.o
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -o binary_search_tree_driver UTFramework.o binary_search_tree.o binary_search_tree_driver.o
