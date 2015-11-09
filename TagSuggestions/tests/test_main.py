from TagSuggestions import main
import unittest as ut

class TestMain(ut.TestCase):
    def test_get_list_index(self):
        index = main.get_list_index(["a", "b", "c"], "c")
        self.assertEqual(index, 2, "get_list_index does not return correct index")

    def test_parse_tags_response(self):
        main.parse_tags_response({
            "items": [
                {"name": "some-tag"},
                {"name": "another-tag"},
                {"name": "unhyphenated"},
                {"name": "why-so-many"},
                {"name": "last-one"}
            ]
        })
        self.assertEqual(main.tagNames, ["some tag", "another tag", "unhyphenated", "why so many", "last one"],
                         "parse_tags_response does not create correct list of tags")

    # Oh boy. This is the big one.
    def test_suggest_tags(self):
        # make sure we've actually got some tag names loaded
        main.tagNames = ["test tag", "suggested", "bot", "another tag"]

        title = "Test question for an automated test in the suggested tags bot code."
        body = "I guess I could just make this body entirely out of key words for the tags, but then again " \
            "I also suppose I'd better craft it well enough that it has a number of cases with which I can test " \
            "what tags get included and what don't.\n\n" \
            "This test was crafted for algorithm revision 2015.11.09.25B.\n\n" \
            " test tag test tag test tag test tag \n\n" \
            " suggested suggested \n\n"
        tags = ["i-dont", "think-these", "actually-matter"]
        related_tags = ["these-do-though", "test tag", "suggested"]

        suggested_tags = main.suggest_tags(title, body, tags, related_tags)
        expected_tags = ["suggested", "test tag"]

        self.assertEqual(suggested_tags, expected_tags, "suggest_tags doesn't suggest correct tags")


def get_tests():
    return ut.TestLoader().loadTestsFromTestCase(TestMain)
