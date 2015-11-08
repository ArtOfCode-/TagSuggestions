import unittest as ut
import TagSuggestions.tests.test_api as api
import TagSuggestions.tests.test_question as question

suites = [
    api.get_tests(),
    question.get_tests()
]

suite = ut.TestSuite()

for tests in suites:
    suite.addTest(tests)

runner = ut.TextTestRunner()
runner.run(suite)