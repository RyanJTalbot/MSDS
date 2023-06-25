import unittest, traceback

class RetroPrinter(unittest.TestResult):
    """
        RetroResult will basically be just like this, assuming 'test' is a
        RetroTestCase.
    """

    def give_result(self, name, status):
        print "RetroGrade Result > " + name + ": " + status

    def complain(self, err):
        error_type = str(err[0])
        error_value = str(err[1])
        error_trace = err[2]
        print error_value
        traceback.print_tb(error_trace)

    def addSuccess(self, test):
        self.give_result(test.outputName, "+")

    def addFailure(self, test, err):
        self.give_result(test.outputName, "-")
        self.complain(err)

    def addError(self, test, err):
        self.give_result(test.outputName, "-")
        self.complain(err)
