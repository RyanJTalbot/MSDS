# This top block is all you will probably need to change
STUDENT_IMPL_FILE 	= huffman.cpp
STUDENT_OBJ_FILE 	= huffman.o
PRIMARY_HEADER_FILE 	= huffman.h
UNIT_TEST_IMPL_FILE 	= huffman_driver.cpp
UNIT_TEST_OBJ_FILE 	= huffman_driver.o
UNIT_TEST_BINARY 	= huffman_driver
MANUAL_DRIVER	 	= huffman

# Other object files needed in building targets for unit testing
FRAMEWORK_TARGETS	= UTFramework.o

USER_DIR = .
CPPFLAGS += -pthread \
	-g \
	-std=c++0x \
	-Wreturn-type \
	-Wunused-variable

# House-keeping build targets.

all : $(UNIT_TEST_BINARY)

clean :
	rm -f $(TESTS) *.o $(UNIT_TEST_BINARY) $(MANUAL_DRIVER)

# Assignment-specific build rules below.

UTFramework.o: $(USER_DIR)/UTFramework.cpp	\
                 $(USER_DIR)/UTFramework.h
	$(CXX) $(CPPFLAGS) -c $(USER_DIR)/UTFramework.cpp

huffman_help.o: $(USER_DIR)/huffman_help.cpp	\
                 $(USER_DIR)/huffman.h
	$(CXX) $(CPPFLAGS) -c $(USER_DIR)/huffman_help.cpp

$(STUDENT_OBJ_FILE): $(USER_DIR)/$(STUDENT_IMPL_FILE) \
                $(USER_DIR)/$(PRIMARY_HEADER_FILE) \
                $(FRAMEWORK_TARGETS)
	$(CXX) $(CPPFLAGS) -c $(USER_DIR)/$(STUDENT_IMPL_FILE) -o $(STUDENT_OBJ_FILE)

$(UNIT_TEST_OBJ_FILE) : $(USER_DIR)/$(UNIT_TEST_IMPL_FILE) \
                     $(USER_DIR)/$(PRIMARY_HEADER_FILE) \
                     $(FRAMEWORK_TARGETS)
	$(CXX) $(CPPFLAGS) -c $(USER_DIR)/$(UNIT_TEST_IMPL_FILE)

$(UNIT_TEST_BINARY) : $(STUDENT_OBJ_FILE) $(UNIT_TEST_OBJ_FILE) \
		   $(FRAMEWORK_TARGETS) huffman_help.o
	$(CXX) $(CPPFLAGS) $^ -o $@

$(MANUAL_DRIVER): $(STUDENT_OBJ_FILE) huffman_help.o
	$(CXX) $(CPPFLAGS) $^ -o $@
