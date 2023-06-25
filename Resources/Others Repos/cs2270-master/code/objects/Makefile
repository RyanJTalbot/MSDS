# This top block is all you will probably need to change
STUDENT_IMPL_FILE 	= LinkedList.cpp
STUDENT_OBJ_FILE 	= LinkedList.o
PRIMARY_HEADER_FILE 	= LinkedList.hpp
DRIVER			= linked_list

USER_DIR = .
CPPFLAGS += -I$(GTEST_DIR)/include
CXXFLAGS += -g -Wall -Wextra -std=c++0x

# House-keeping build targets.

all : $(DRIVER)

clean :
	rm -f $(TESTS) *.o $(DRIVER)

# Assignment-specific build rules below.

$(STUDENT_OBJ_FILE): $(USER_DIR)/$(STUDENT_IMPL_FILE) \
                $(USER_DIR)/$(PRIMARY_HEADER_FILE) \
                $(FRAMEWORK_TARGETS)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/$(STUDENT_IMPL_FILE) -o $(STUDENT_OBJ_FILE)

$(DRIVER) : $(STUDENT_OBJ_FILE) 
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -Qunused-arguments -pthread $^ -o $@



