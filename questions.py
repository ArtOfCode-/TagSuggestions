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
        self.id = api_item["question_id"]
        self.body = api_item["body"]
        self.tags = api_item["tags"]
        self.title = api_item["title"]
        self.score = int(api_item["score"])
        if "closed_date" in api_item and api_item["closed_date"] is not None:
            self.closed = True
        else:
            self.closed = False
