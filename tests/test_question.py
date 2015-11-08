import questions
from unittest import TestCase


class TestQuestion(TestCase):
    dummy_item = {
        "question_id": 20477,
        "body": "lots and lots of text in here that I can't be bothered to type out",
        "tags": ["some-tag", "something-else", "alloneword", "aah-tags"],
        "title": "not a real question",
        "score": -99
    }

    dummy_closed_item = {
        "question_id": 20477,
        "body": "lots and lots of text in here that I can't be bothered to type out",
        "tags": ["some-tag", "something-else", "alloneword", "aah-tags"],
        "title": "not a real question",
        "score": 99,
        "closed_date": "2015-11-08 18:23Z"
    }

    dummy_clear_item = {
        "question_id": 20477,
        "body": "lots and lots of text in here that I can't be bothered to type out",
        "tags": ["some-tag", "something-else", "alloneword", "aah-tags"],
        "title": "not a real question",
        "score": 99
    }

    dummy_error_item = {
        "question_id": 20477,
        "oh_no_missing_body": "",
        "tags": None,
        "title": "not a real question",
        "score": -99
    }

    filter = questions.QuestionFilter({"score": 1, "closed": False})

    def test_question_init(self):
        try:
            questions.Question(self.dummy_item)
        except:
            self.fail("questions.Question.__init__ throws unexpected error")

    def test_question_error_init(self):
        try:
            questions.Question(self.dummy_error_item)
        except KeyError:
            pass
        else:
            self.fail("questions.Question.__init__ doesn't throw KeyError")

    def test_filter_filter(self):
        score_filter = self.filter.filter(questions.Question(self.dummy_item))
        closed_filter = self.filter.filter(questions.Question(self.dummy_closed_item))
        clear_filter = self.filter.filter(questions.Question(self.dummy_clear_item))
        self.assertTrue(not score_filter)
        self.assertTrue(not closed_filter)
        self.assertTrue(clear_filter)

    def test_filter_error(self):
        try:
            self.filter.filter(None)
        except questions.FilterException:
            pass
        else:
            self.fail("questions.QuestionFilter.filter doesn't throw questions.FilterException")
