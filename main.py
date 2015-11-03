from api import APIRequester
import time
import sys

tagNames = []
apiManager = None

def get_list_index(list, item, alternative):
    try:
        return list.index(item)
    except:
        try:
            return list.index(alternative)
        except:
            return None

def main():
    global apiManager

    if "-s" in sys.argv or "--site" in sys.argv:
        index = get_list_index(sys.argv, "-s", "--site")
        if len(sys.argv) >= index + 2:
            apiManager = APIRequester(sys.argv[index + 1])
        else:
            print("[System] [WARNING] No site specified after -s or --site switch.")
    else:
        apiManager = APIRequester("hardwarerecs")

    get_tags()
    print()

    if "-a" in sys.argv or "--all" in sys.argv:
        questions = get_all_questions()
        print()
        print_suggested_tags(questions)
    elif "-i" in sys.argv or "--ids" in sys.argv:
        index = get_list_index(sys.argv, "-i", "--ids") + 1
        ids = []
        ids.append(sys.argv[index][1:])
        index += 1
        while True:
            if "]" not in sys.argv[index]:
                ids.append(sys.argv[index])
                index += 1
            else:
                ids.append(sys.argv[index][:-1])
                break
        questions = get_questions(ids)
        print()
        print_suggested_tags(questions)


def print_suggested_tags(questions):
    if questions is not None:
        for question in questions:
            print("Tag suggestions for question #{0}".format(question["id"]))
            suggested_tags = suggest_tags(question["body"], question["tags"])

            scored_tags = []
            for k, v in suggested_tags:
                if v >= 6:
                    scored_tags.append(k)

            if len(scored_tags) == 0:
                print("No tag suggestions for this question.")
            else:
                print(", ".join(scored_tags))
                input("Press <Enter> to continue.")
            print()

def get_tags():
    """
    Gets the API data for all tags on the site. Delegates processing of the data - see parse_tags_response.
    :return: None. This is a purely operational method.
    """
    tag_filter = ".IrqzSiB8kWl"
    has_more = True
    page = 1

    while has_more:
        print("Retrieving page #{0} of tags...".format(page))
        response, has_even_more, backoff = apiManager.request("/tags", {'filter': tag_filter, 'pagesize': 100, 'page': page})
        has_more = has_even_more

        parse_tags_response(response)

        if backoff > 0:
            print("Back-off received. Waiting {0} seconds before trying again.".format(backoff))
            time.sleep(backoff)

        page += 1

    print("Finished processing all tags.")

def get_question(id):
    """
    Gets a single question from its ID.
    :param id: The ID of the question to fetch.
    :return: Four values: the title, body, tags, and ID of the question.
    """
    question_filter = "!5-dm_.B4H9w)5lg0TAHAdqVJfRO)Oe)ur3etgG"

    print("Fetching question #{0}...".format(id))

    response, has_more, backoff = apiManager.request("/questions/" + str(id), {'filter': question_filter})

    if "error_id" in response:
        print("[API] [ERROR] Could not fetch question #{0}: ID {1}, name '{2}', message '{3}'".format(response["error_id"],
                                                                                       response["error_name"],
                                                                                       response["error_message"]))
        return
    else:
        item = response["items"][0]
        if "closed_date" not in item or ("closed_date" in item and item["closed_date"] is None):
            return item["title"], item["body"], item["tags"], item["question_id"]
        else:
            return None

def get_questions(ids):
    """
    Gets a list of question objects, one for each ID passed in ids.
    :param ids: A list of IDs to return question objects for.
    :return: A list of objects representing questions, each with title, body, and tags fields.
    """
    if len(ids) > 100:
        print("[System] [ERROR] Number of IDs passed to get_questions(ids) cannot be > 100.")
        return

    questions = []
    question_filter = "!5-dm_.B4H9w)5lg0TAHAdqVJfRO)Oe)ur3etgG"

    id_list = ";".join(ids)

    print("Fetching questions #" + ", #".join(ids) + "...")

    response, has_more, backoff = apiManager.request("/questions/{0}".format(id_list), {'filter': question_filter})

    if "error_id" in response:
        print("[API] [ERROR] Could not fetch question #{0}: ID {1}, name '{2}', message '{3}'".format(response["error_id"],
                                                                                       response["error_name"],
                                                                                       response["error_message"]))
        return
    else:
        for item in response["items"]:
            if "closed_date" not in item or ("closed_date" in item and item["closed_date"] is None):
                questions.append({'title': item["title"], 'body': item["body"], 'tags': item["tags"], 'id': item["question_id"]})
            else:
                print("Question #" + str(item["question_id"]) + " is closed.")

    return questions

def get_all_questions():
    questions = []
    question_filter = "!5-dm_.B4H9w)5lg0TAHAdqVJfRO)Oe)ur3etgG"
    has_more = True
    page = 1

    while has_more:
        print("Fetching page #{0} of questions...".format(page))
        response, has_even_more, backoff = apiManager.request("/questions", {'filter': question_filter, 'pagesize': 100, 'page': page})
        has_more = has_even_more

        if "error_id" in response:
            print("[API] [ERROR] Could not fetch questions: ID {0}, name '{1}', message '{2}'.".format(response["error_id"],
                                                                                                       response["error_name"],
                                                                                                       response["error_message"]))
            return
        else:
            for item in response["items"]:
                if "closed_date" not in item or ("closed_date" in item and item["closed_date"] is None):
                    questions.append({'title': item["title"], 'body': item["body"], 'tags': item["tags"], 'id': item["question_id"]})

        if backoff > 0:
            print("Back-off received, waiting {0} seconds before repeating request.".format(backoff))
            time.sleep(backoff)

        page += 1

    return questions

def get_related_tags(tags):
    """
    Gets a list of tags that the Stack Exchange engine considers related to the tags given.
    :param tag_name: A list of tag names to find related tags for.
    :return: A list containing names of related tags.
    """
    while len(tags) > 4:
        del tags[-1]

    tag_filter = ".IrqzSiB8kWl"
    tag_string = ";".join(tags)

    response, has_more, backoff = apiManager.request("/tags/{0}/related".format(tag_string), {'filter': tag_filter})

    if "error_id" in response:
        print("[API] [ERROR] Could not get related tags: ID {0}, name '{1}', message '{2}'.".format(response["error_id"],
                                                                                                    response["error_name"],
                                                                                                    response["error_message"]))
        return
    else:
        tags = []
        for item in response["items"]:
            tags.append(item["name"].replace("-", " "))
        return tags

def parse_tags_response(response):
    """
    Populates a list of tag names based on an API response.
    :param response: An API response object, where items is a list of tag objects.
    :return: None. However, the tagNames variable is populated by this method.
    """
    if "error_id" in response:
        print("[API] [ERROR] Could not fetch tags: ID {0}, name '{1}', message '{2}'.".format(response["error_id"],
                                                                               response["error_name"],
                                                                               response["error_message"]))
        return
    else:
        for item in response["items"]:
            tagNames.append(item["name"].replace("-", " "))

def suggest_tags(body, tags):
    """
    Suggests tags for a question, based on its body and current tags.
    :param body: The question's body text.
    :param tags: A list of the tags on the question, as returned by the API.
    :return: A list containing suggested tag names.
    """
    body = body.lower()

    suggested_tags = {}

    for tag_name in tagNames:
        if " " + tag_name + " " in body:
            if tag_name in suggested_tags:
                suggested_tags[tag_name] += 2
            else:
                suggested_tags[tag_name] = 2

    related_tags = get_related_tags(tags)
    for tag in related_tags:
        if tag in suggested_tags:
            suggested_tags[tag] += 1
        else:
            suggested_tags[tag] = 1
        if " " + tag + " " in body:
            if tag in suggested_tags:
                suggested_tags[tag] += 3
            else:
                suggested_tags[tag] = 3

    remove_tags = []
    for tag, score in suggested_tags.items():
        if tag in tags:
            remove_tags.append(tag)

    for tag in remove_tags:
        del suggested_tags[tag]

    sorted_tags = sorted(suggested_tags.items(), key = lambda x: x[1], reverse = True)
    while len(sorted_tags) > (5 - len(tags)):
        del sorted_tags[-1]

    return sorted_tags




main()
