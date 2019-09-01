from hostingde.api.errors import ApiHttpStatusCodeError, ApiResponseError
from hostingde.api.filter import BaseFilter
import json
import requests
import logging


logger = logging.getLogger(__name__)


class RequestHandler:
    """ This class is designed to allow easy interaction with the Hosting.de DNS API."""

    def __init__(self, auth_token=None, base_url="https://secure.hosting.de"):
        self.__auth_token = auth_token
        self.__base_url = base_url

    def set_auth_token(self, auth_token):
        self.__auth_token = auth_token

    def set_base_url(self, base_url):
        self.__base_url = base_url

    def get_api_response(self, path, data):

        data["authToken"] = self.__auth_token
        url = self.__base_url + path

        logger.debug("requesting from api: {}".format(url))
        response = requests.post(
            url, json.dumps(data), headers={"Content-Type": "application/json"}
        )

        if response.status_code != 200:
            raise ApiHttpStatusCodeError(url, response.status_code)

        response_data = json.loads(response.content)
        logger.debug(
            "response content from api call to {} returned with status: {} [warnings: {} / errors: {}]".format(
                response.url,
                response_data["status"],
                len(response_data["warnings"]),
                len(response_data["errors"]),
            )
        )
        for warning in response_data["warnings"]:
            logger.warning(
                "request to {} responded with warning: [{}]: {}".format(
                    response.url, warning["code"], warning["text"]
                )
            )
        for error in response_data["errors"]:
            logger.error(
                "request to {} responded with error: [{}]: {}".format(
                    response.url, error["code"], error["text"]
                )
            )

        if response_data["status"] != "success" and len(response_data["errors"]) > 0:
            error = response_data["errors"][0]
            raise ApiResponseError(response.url, error["text"], error["code"])

        return response, response_data

    def get_filtered_api_response(self, path, filter, limit, page, sort):
        return self.get_api_response(
            path, self.get_filter_request_data(filter, limit, page, sort)
        )

    @staticmethod
    def get_filter_request_data(filter, limit, page, sort):

        if issubclass(filter.__class__, BaseFilter):
            filter_data = filter.get_filter_data()
        else:
            filter_data = filter

        return {"filter": filter_data, "limit": limit, "page": page, "sort": sort}
