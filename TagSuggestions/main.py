if __name__ == "__main__":
    from api import APIRequester, APIException
    from questions import *
    from database import *
    import mysql.connector as mysql
else:
    from .api import APIRequester, APIException
    from .questions import *

import time
import sys
import re
import getpass

tagNames = []
blacklistedTagNames = []

apiManager = None
queryManager = None

questionFilter = QuestionFilter({
    'score': 1,
    'closed': False
})

dbCredentials = {
    'host': None,
    'user': None,
    'pass': None,
    'name': None
}

siteName = ""


def get_list_index(list_obj, item, alternative=None):
    try:
        return list_obj.index(item)
    except:
        if alternative is not None:
            try:
                return list_obj.index(alternative)
            except:
                return None
        else:
            return None


def populate_db_creds():
    if "--db-host" in sys.argv and "--db-user" in sys.argv and "--db-name" in sys.argv:
        host_index = get_list_index(sys.argv, "--db-host") + 1
        user_index = get_list_index(sys.argv, "--db-user") + 1
        name_index = get_list_index(sys.argv, "--db-name") + 1
        if len(sys.argv) >= host_index:
            dbCredentials['host'] = sys.argv[host_index]
        if len(sys.argv) >= user_index:
            dbCredentials['user'] = sys.argv[user_index]
        if len(sys.argv) >= name_index:
            dbCredentials['name'] = sys.argv[name_index]
        dbCredentials['pass'] = getpass.getpass("Database password: ")
        return True
    else:
        return False



def main():
    global apiManager
    global queryManager
    global siteName

    db_available = populate_db_creds()
    print()
    if db_available:
        try:
            queryManager = QueryManager(dbCredentials['host'], dbCredentials['user'], dbCredentials['pass'],
                                        dbCredentials['name'])
        except mysql.Error as ex:
            if ex.errno == mysql.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Error connecting to database: access denied. Username/password combination is incorrect.")
            elif ex.errno == mysql.errorcode.ER_BAD_DB_ERROR:
                print("Error connecting to database: DB does not exist.")
            else:
                print("Error connecting to database:")
                print(ex)
            db_available = False

    if "-s" in sys.argv or "--site" in sys.argv:
        index = get_list_index(sys.argv, "-s", "--site")
        if len(sys.argv) >= index + 2:
            siteName = sys.argv[index + 1]
        else:
            print("[System] [WARNING] No site specified after -s or --site switch.")
            siteName = "hardwarerecs"
    else:
        siteName = "hardwarerecs"

    apiManager = APIRequester(siteName)

    if db_available:
        get_blacklisted_tags()
        print("{0} blacklisted tags for this site.".format(str(len(blacklistedTagNames))))
        print()

    get_tags()
    print()

    if "-a" in sys.argv or "--all" in sys.argv:
        questions = get_all_questions()
        print()
        print_suggested_tags(questions)
    elif "-i" in sys.argv or "--ids" in sys.argv:
        index = get_list_index(sys.argv, "-i", "--ids") + 1
        ids = []
        if len(sys.argv) == 3:
            ids.append(sys.argv[index][1:-1])
        else:
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

    queryManager.dispose()


def print_suggested_tags(questions):
    if questions is not None:
        for question in questions:
            print("Tag suggestions for question #{0}".format(question.id))
            suggested_tags = suggest_tags(question.title, question.body, question.tags)

            if len(suggested_tags) == 0:
                print("No tag suggestions for this question.")
            else:
                print(", ".join(suggested_tags))
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

    while has_more and page <= 8:
        print("Retrieving page #{0} of tags...".format(page))

        try:
            response, has_even_more, backoff = apiManager.request("/tags", {'filter': tag_filter, 'pagesize': 100,
                                                                            'page': page})
            has_more = has_even_more

            parse_tags_response(response)

            if backoff > 0:
                print("Back-off received. Waiting {0} seconds before trying again.".format(backoff))
                time.sleep(backoff)

            page += 1
        except APIException as ex:
            print("[API] [ERROR] Could not fetch tags: #{0} '{1}' - {2}".format(ex.id, ex.name, ex.message))
            continue

    print("Finished processing all tags.")


def get_blacklisted_tags():
    """
    Retrieves and processes a list of blacklisted tags from a database.
    :return: None - but the blacklistedTagNames object is populated.
    """
    global queryManager
    results = queryManager.query("SELECT TagName, SiteName FROM BlacklistedTags WHERE SiteName = '{sn}';", {
        "sn": siteName
    })
    for (tag) in results:
        blacklistedTagNames.append(tag[0])
    queryManager.dispose(results)


def get_question(question_id):
    """
    Gets a single question from its ID.
    :param question_id: The ID of the question to fetch.
    :return: Four values: the title, body, tags, and ID of the question.
    """
    question_filter = "!gB66oJbwvgwG7j98E2D9v2aYulgjnMOAQ0S"

    print("Fetching question #{0}...".format(question_id))

    try:
        response, has_more, backoff = apiManager.request("/questions/" + str(question_id), {'filter': question_filter})
        item = response["items"][0]
        question = Question(item)
        if questionFilter.filter(question):
            return question
        else:
            print("Question #{0} does not meet requirements to suggest tags for.".format(question.id))
            return None
    except APIException as ex:
        print("[API] [ERROR] Could not fetch question: #{0} '{1}' - {2}".format(ex.id, ex.name, ex.message))
        return None


def get_questions(ids):
    """
    Gets a list of question objects, one for each ID passed in ids.
    :param ids: A list of IDs to return question objects for.
    :return: A list of Question objects.
    """
    if len(ids) > 100:
        print("[System] [ERROR] Number of IDs passed to get_questions(ids) cannot be > 100.")
        return

    questions = []
    question_filter = "!gB66oJbwvgwG7j98E2D9v2aYulgjnMOAQ0S"

    id_list = ";".join(ids)

    print("Fetching questions #" + ", #".join(ids) + "...")

    try:
        response, has_more, backoff = apiManager.request("/questions/{0}".format(id_list), {'filter': question_filter})
        for item in response["items"]:
            question = Question(item)
            if questionFilter.filter(question):
                questions.append(question)
            else:
                print("Question #{0} does not meet requirements to suggest for.".format(question.id))

        return questions
    except APIException as ex:
        print("[API] [ERROR] Could not fetch questions: #{0} '{1}' - {2}".format(ex.id, ex.name, ex.message))
        return None


def get_all_questions():
    """
    Gets a list of questions, based on most recently active.
    :return: A list of Question objects.
    """
    questions = []
    question_filter = "!gB66oJbwvgwG7j98E2D9v2aYulgjnMOAQ0S"
    has_more = True
    page = 1

    while has_more and page <= 10:
        print("Fetching page #{0} of questions...".format(page))

        try:
            response, has_even_more, backoff = apiManager.request("/questions", {'filter': question_filter,
                                                                                 'pagesize': 100, 'page': page})
            has_more = has_even_more

            for item in response["items"]:
                question = Question(item)
                if questionFilter.filter(question):
                    questions.append(question)

            if backoff > 0:
                print("Back-off received, waiting {0} seconds before repeating request.".format(backoff))
                time.sleep(backoff)

            page += 1
        except APIException as ex:
            print("[API] [ERROR] Could not fetch questions: #{0} '{1}' - {2}".format(ex.id, ex.name, ex.message))
            return None

    return questions


def get_related_tags(tags):
    """
    Gets a list of tags that the Stack Exchange engine considers related to the tags given.
    :param tags: A list of tag names to find related tags for.
    :return: A list containing names of related tags.
    """
    while len(tags) > 4:
        del tags[-1]

    tag_filter = ".IrqzSiB8kWl"
    tag_string = ";".join(tags)

    try:
        response, has_more, backoff = apiManager.request("/tags/{0}/related".format(tag_string), {'filter': tag_filter})
        tags = []
        for item in response["items"]:
            tags.append(item["name"].replace("-", " "))
        return tags
    except APIException as ex:
        print("[API] [ERROR] Could not fetch tags: #{0} '{1}' - {2}".format(ex.id, ex.name, ex.message))
        return None


def parse_tags_response(response):
    """
    Populates a list of tag names based on an API response.
    :param response: An API response object, where items is a list of tag objects.
    :return: None. However, the tagNames variable is populated by this method.
    """
    for item in response["items"]:
        tagNames.append(item["name"].replace("-", " "))


# Algorithm revision 2015.11.16.27B
def suggest_tags(title, body, tags, related_tags=None, verbose=False):
    """
    Suggests tags for a question, based on its body and current tags.
    :param body: The question's body text.
    :param tags: A list of the tags on the question, as returned by the API.
    :return: A list containing suggested tag names.
    """
    body = body.lower()

    # remove anything in a preformatted code span; these were causing errors
    re.sub(r'<pre>(.*?)</pre>', '', body, flags=re.DOTALL)

    suggested_tags = {}

    for tag_name in tagNames:
        if verbose: print("Checking tag name: {0}".format(tag_name))
        if " " + tag_name + " " in body:
            count = body.count(" " + tag_name + " ") * 2  # * 2 because it was returning half-count for some reason
            if verbose: print("Tag in body: +{0} instances".format(str(count)))
            if tag_name in suggested_tags:
                suggested_tags[tag_name] += count
            else:
                suggested_tags[tag_name] = count
        if " " + tag_name + " " in title:
            if verbose: print("Tag in title: +2")
            if tag_name in suggested_tags:
                suggested_tags[tag_name] += 2
            else:
                suggested_tags[tag_name] = 2

    if related_tags is None:
        related_tags = get_related_tags(tags)

    if related_tags is not None:
        for tag in iter(related_tags):
            if verbose: print("Related tag '{0}' +1".format(tag))
            if tag in suggested_tags:
                suggested_tags[tag] += 1
            else:
                suggested_tags[tag] = 1
            if " " + tag + " " in body:
                if verbose: print("Related tag in body: +2")
                if tag in suggested_tags:
                    suggested_tags[tag] += 2
                else:
                    suggested_tags[tag] = 2

    remove_tags = []
    for tag, score in suggested_tags.items():
        if tag in tags:
            if verbose: print("Tag '{0}' already on question: remove".format(tag))
            remove_tags.append(tag)
        if tag in blacklistedTagNames and tag not in remove_tags:
            if verbose: print("Tag '{0}' in blacklist: remove".format(tag))
            remove_tags.append(tag)
        blacklisted_string = " ".join(blacklistedTagNames)
        if tag in blacklisted_string and tag not in remove_tags:
            if verbose: print("Tag {0} is a superset of blacklisted tag: remove".format(tag))
            remove_tags.append(tag)
        tags_string = " ".join(tags)
        if tag in tags_string and tag not in remove_tags:
            if verbose: print("Tag '{0}' is a superset of question tag: remove".format(tag))
            remove_tags.append(tag)

    for tag in remove_tags:
        del suggested_tags[tag]

    sorted_tags = sorted(suggested_tags.items(), key=lambda x: x[1], reverse=True)
    while len(sorted_tags) > (5 - len(tags)):
        del sorted_tags[-1]

    scored_tags = []
    if verbose: print("Tags sorted by score:")
    for k, v in sorted_tags:
        if verbose: print("'{0}': {1}".format(k, str(v)))
        if v >= 7:
            scored_tags.append(k)

    return scored_tags

if __name__ == "__main__":
    main()
