import requests


class APIRequester:
    """
    Manages requests to and responses from the Stack Exchange API.
    """

    def __init__(self, site):
        """
        Initialises a new APIRequester object, setting default values.
        :return: A new APIRequester.
        """
        self.client_id = 5902
        self.request_key = "GNSUb6CLudN5uRhiJfQ9Qg(("
        self.remaining_quota = None
        self.site = site

    def request(self, path, data):
        """
        Executes a request to the Stack Exchange API.
        :param path: The method to request, such as /questions or /tags. No need for /2.2 prefix.
        :param data: An object, containing data that will be passed in the GET request to the API.
        :return: Three values: the API response, the has_more parameter, and the backoff parameter.
        """
        if data is None:
            data = {}

        request_string = "?key=" + self.request_key + "&site=" + self.site + "&"
        for key, value in data.items():
            request_string += key + "=" + str(value) + "&"

        request_url = "https://api.stackexchange.com/2.2" + path + request_string
        response = requests.get(request_url, timeout=20).json()

        has_more = False
        backoff = 0

        if "error_id" in response:
            raise APIException(response["error_id"], response["error_name"], response["error_message"])

        if "quota_remaining" in response:
            self.remaining_quota = response["quota_remaining"]
        if "has_more" in response and response["has_more"] is True:
            has_more = True
        if "backoff" in response:
            backoff = int(response["backoff"])

        return response, has_more, backoff


class APIException(BaseException):
    """
    Represents an error returned from the Stack Exchange API.
    """

    def __init__(self, e_id, name, message):
        """
        Initialises a new APIException object. All parameters can be found in API responses.
        :param e_id: The SEAPI error ID.
        :param name: The SEAPI error name.
        :param message: The SEAPI error message.
        :return: A new APIException.
        """
        self.id = e_id
        self.name = name
        self.message = message
