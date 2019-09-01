from hostingde.api.clients.core import RequestHandler

QUERY_LIMIT = 25


class DnsClient:
    """ This class is designed to allow easy interaction with the Hosting.de DNS API."""

    def __init__(self, auth_token=None, *args, **kwargs):
        self.__api = kwargs.get("api", RequestHandler(auth_token))

    def set_request_handler(self, request_handler):
        self.__api = request_handler

    def set_auth_token(self, auth_token):
        self.__api.set_auth_token(auth_token)

    def set_base_url(self, base_url):
        self.__api.set_base_url(base_url)

    # internal api helper functions

    def __get_api_data(self, path, data):
        response = self.__api.get_api_response(path, data)
        return response[1]["response"]

    def __get_filtered_api_data(self, path, filter, limit, page, sort):
        response = self.__api.get_filtered_api_response(path, filter, limit, page, sort)
        return response[1]["response"]

    # hosting.de api list functions

    def find_zone_configs(self, zone_filter, limit=QUERY_LIMIT, page=1, sort=None):
        """Hosting.de api function for listing zone configs - https://www.hosting.de/api/#list-zoneconfigs"""
        return self.__get_filtered_api_data(
            "/api/dns/v1/json/zoneConfigsFind", zone_filter, limit, page, sort
        )

    def find_zones(self, zone_filter, limit=QUERY_LIMIT, page=1, sort=None):
        """Hosting.de api function for listing zones - https://www.hosting.de/api/#listing-zones"""
        return self.__get_filtered_api_data(
            "/api/dns/v1/json/zonesFind", zone_filter, limit, page, sort
        )

    def find_records(self, record_filter, limit=QUERY_LIMIT, page=1, sort=None):
        """Hosting.de api function for listing records - https://www.hosting.de/api/#listing-records"""
        return self.__get_filtered_api_data(
            "/api/dns/v1/json/recordsFind", record_filter, limit, page, sort
        )

    # hosting.de api zone editing functions

    def create_zone(self, zone_config, records, use_default_nss=False, nss_id=0):
        """Hosting.de api function for creating a zone - https://www.hosting.de/api/#creating-new-zones"""
        return self.__get_api_data(
            "/api/dns/v1/json/zoneCreate",
            {
                "zoneConfig": zone_config,
                "records": records,
                "useDefaultNameserverSet": use_default_nss,
                "nameserverSetId": nss_id,
            },
        )

    def recreate_zone(self, zone_config, records, use_default_nss=False, nss_id=0):
        """Hosting.de api function for recreating a zone - https://www.hosting.de/api/#recreating-existing-zones"""
        return self.__get_api_data(
            "/api/dns/v1/json/zoneRecreate",
            {
                "zoneConfig": zone_config,
                "records": records,
                "useDefaultNameserverSet": use_default_nss,
                "nameserverSetId": nss_id,
            },
        )

    def delete_zone(self, zone_name=None, zone_config_id=None):
        """Hosting.de api function for deleting a zone - https://www.hosting.de/api/#deleting-zones"""
        data = {}
        if zone_config_id:
            data["zoneConfigId"] = zone_config_id
        elif zone_name:
            data["zoneName"] = zone_name

        return self.__get_api_data("/api/dns/v1/json/zoneDelete", data)

    def update_zone(self, zone_config, records_to_add=[], records_to_delete=[]):
        """Hosting.de api function for updating a zone - https://www.hosting.de/api/#updating-zones"""
        return self.__get_api_data(
            "/api/dns/v1/json/zoneUpdate",
            {
                "zoneConfig": zone_config,
                "recordsToAdd": records_to_add,
                "recordsToDelete": records_to_delete,
            },
        )
