

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
    """Exception raised for errors with bad https status code.

    Attributes:
        url -- url used to connect to
        message -- explanation of the error
        status_code -- code of the http response
    """

    def __init__(self, url, message, status_code):
        self.url = url
        self.message = message
        self.status_code = status_code


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
