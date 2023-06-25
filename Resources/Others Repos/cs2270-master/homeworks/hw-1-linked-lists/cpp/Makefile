# Where to find user code.
USER_DIR = .

# Flags passed to the preprocessor.
CPPFLAGS =

# Flags passed to the C++ compiler.
CXXFLAGS = -g -Wall -Wextra

# House-keeping build targets.

all : linked_list_driver

clean :
	rm -f *.o

# Assignment-specific build rules below.

linked_list.o : $(USER_DIR)/linked_list.cpp \
                $(USER_DIR)/linked_list.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/linked_list.cpp

linked_list_driver: linked_list.o linked_list_driver.o
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -o linked_list_driver linked_list.o linked_list_driver.cpp
