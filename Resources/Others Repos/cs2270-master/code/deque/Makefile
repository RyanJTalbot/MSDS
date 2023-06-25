# This top block is all you will probably need to change
STUDENT_IMPL_FILE 	= deque.cpp
STUDENT_OBJ_FILE 	= deque.o
PRIMARY_HEADER_FILE 	= deque.h
MANUAL_TEST_IMPL_FILE 	= deque_driver.cpp
MANUAL_TEST_OBJ_FILE 	= deque_driver.o
MANUAL_TEST_BINARY 	= deque_driver
UNIT_TEST_IMPL_FILE 	= deque_unittest.cpp
UNIT_TEST_OBJ_FILE 	= deque_unittest.o
UNIT_TEST_BINARY 	= deque_unittest

# Other object files needed in building targets for unit testing
FRAMEWORK_TARGETS	= UTFramework.o

USER_DIR = .
CPPFLAGS += -I$(GTEST_DIR)/include
CXXFLAGS += -g -Wall -Wextra -std=c++0x

# combined things
BINARIES = $(UNIT_TEST_BINARY) $(MANUAL_TEST_BINARY)

# House-keeping build targets.

all : $(BINARIES)

clean :
	rm -f $(TESTS) *.o $(BINARIES)

# Assignment-specific build rules below.

UTFramework.o: $(USER_DIR)/UTFramework.cpp	\
                 $(USER_DIR)/UTFramework.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/UTFramework.cpp

$(STUDENT_OBJ_FILE): $(USER_DIR)/$(STUDENT_IMPL_FILE) \
                $(USER_DIR)/$(PRIMARY_HEADER_FILE) \
                $(FRAMEWORK_TARGETS)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/$(STUDENT_IMPL_FILE) -o $(STUDENT_OBJ_FILE)

$(UNIT_TEST_OBJ_FILE) : $(USER_DIR)/$(UNIT_TEST_IMPL_FILE) \
                     $(USER_DIR)/$(PRIMARY_HEADER_FILE) \
                     $(FRAMEWORK_TARGETS)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/$(UNIT_TEST_IMPL_FILE)

$(MANUAL_TEST_OBJ_FILE) : $(USER_DIR)/$(MANUAL_TEST_IMPL_FILE) \
                     $(USER_DIR)/$(PRIMARY_HEADER_FILE)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/$(MANUAL_TEST_IMPL_FILE)

$(UNIT_TEST_BINARY) : $(STUDENT_OBJ_FILE) $(UNIT_TEST_OBJ_FILE) \
		   $(FRAMEWORK_TARGETS)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -pthread $^ -o $@

$(MANUAL_TEST_BINARY) : $(STUDENT_OBJ_FILE) $(MANUAL_TEST_OBJ_FILE)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -pthread $^ -o $@



