class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class ObjectNotFoundError(Error):
    """Exception raised for errors with objects that cannot be found.
    
     Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class ApiHttpStatusError(Error):
    """Exception raised for errors with bad http status code.

    Attributes:
        url -- url used to connect to
        message -- explanation of the error
        status_code -- code of the http response
    """

    def __init__(self, url, message, status_code):
        self.url = url
        self.message = message
        self.status_code = status_code


def get_status_code_message(status_code, url):
    HTTP_STATUS_CODE_MESSAGES = {
        200: "OK",
        400: "The HTTP request was malformed",
        404: "Method, format, or entry point not found",
        405: "Method not allowed",
        500: "Internal server error",
        502: "Server temporarily not available",
        503: "Server temporarily not available due to maintenance",
        504: "Backend timeout",
    }

    code_message = HTTP_STATUS_CODE_MESSAGES.get(status_code, "Unknown HTTP StatusCode")

    return "Hosting.de Api returned HTTP{} at {} - {}.".format(
        status_code, url, code_message
    )


class ApiHttpStatusCodeError(Error):
    """Exception raised for errors with bad http status code.

    Attributes:
        url -- url used to connect to
        status_code -- code of the http response
        message -- explanation of the error
    """

    def __init__(self, url, status_code):
        self.url = url
        self.status_code = status_code
        self.message = get_status_code_message(status_code, url)


class ApiResponseError(Error):
    """Exception raised for errors with bad http status code.

    Attributes:
        url -- url used to connect to
        message -- explanation of the error
        status_code -- code of the http response
    """

    def __init__(self, url, message, errors):
        self.url = url
        self.message = message
        self.errors = errors
