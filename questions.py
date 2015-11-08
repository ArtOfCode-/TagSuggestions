# QUESTIONS API FILTERING
#
# The questions API filter is currently '!gB66oJbwvgwG7j98E2D9v2aYulgjnMOAQ0S'.
# It contains:
#
# - near-default .wrapper (minus quota_max field)
# - question.body
# - question.closed_date
# - question.score
# - question.tags
# - question.title
# - question.question_id

class Question:
    def __init__(self, api_item):
        if "question_id" in api_item and "body" in api_item and "tags" in api_item and "title" in api_item \
            and "score" in api_item:
            self.id = api_item["question_id"]
            self.body = api_item["body"]
            self.tags = api_item["tags"]
            self.title = api_item["title"]
            self.score = int(api_item["score"])
        else:
            raise KeyError("not all required values were in the API item")

        if "closed_date" in api_item and api_item["closed_date"] is not None:
            self.closed = True
        else:
            self.closed = False


class QuestionFilter:
    def __init__(self, requirements):
        self.requirements = requirements

    def filter(self, question):
        if not isinstance(question, Question):
            raise FilterException("A Question object must be passed for filtering.")

        if "score" in self.requirements:
            if question.score < self.requirements["score"]:
                return False

        if "closed" in self.requirements:
            if question.closed != self.requirements["closed"]:
                return False
        return True


class FilterException(BaseException):
    pass