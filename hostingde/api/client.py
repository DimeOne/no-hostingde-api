import json
import requests
from hostingde.api.errors import ApiHttpStatusError, ApiResponseError


def getApiResponse(baseUrl, path, data, max_retries=3, retry_delay=2):
    json_data = getApiResponseFullJson(baseUrl, path, data)
    if json_data["status"] != "error":
        return json_data["response"]

    # retry after a given delay, if there is an error, that the object is blocked
    if json_data["errors"][0]["code"] == 10205 and max_retries > 0:
        from time import sleep

        sleep(retry_delay)
        return getApiResponse(baseUrl, path, data, max_retries - 1, retry_delay)

    raise ApiResponseError(path, "Api response returned errors.", json_data["errors"])


def getApiResponseFullJson(baseUrl, path, data):
    response = getApiHttpResponseOrException(baseUrl, path, data)
    return json.loads(response.content)


def getApiHttpResponseOrException(baseUrl, path, data):
    response = getApiHttpResponse(baseUrl, path, data)
    if response.status_code != 200:
        raise ApiHttpStatusError(
            path, "Response did not have a status code of 200.", response.status_code
        )
    return response


def getApiHttpResponse(baseUrl, path, data):
    url = baseUrl + path
    headers = {"Content-Type": "application/json"}
    json_data = json.dumps(data)
    return requests.post(url, json_data, headers=headers)
