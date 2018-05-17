from hostingde.api.errors import ObjectNotFoundError
from hostingde.api.client import getApiResponse
from hostingde.helpers import dns
from hostingde.helpers import filters


class DnsApiClient:

    def __init__(self, authToken, baseUrl='https://secure.hosting.de'):
        self.__authToken = authToken
        self.__baseUrl = baseUrl
    
    # property setters

    def setAuthToken(self, authToken):
        self.__authToken = authToken

    def setBaseUrl(self, baseUrl):
        self.__baseUrl = baseUrl

    # api functions

    def recordFind(self, filter, limit=25, page=1, sort=None):
        data = {
            'authToken': self.__authToken,
            'filter': filter,
            'limit': limit,
            'sort': sort
        }
        return getApiResponse(self.__baseUrl, '/api/dns/v1/json/recordsFind', data)

    def zoneFind(self, filter, limit=25, page=1, sort=None):
        data = {
            'authToken': self.__authToken,
            'filter': filter,
            'limit': limit,
            'sort': sort
        }
        return getApiResponse(self.__baseUrl, '/api/dns/v1/json/zoneFind', data)

    def zoneUpdate(self, zoneConfig, recordsToAdd, recordsToDelete=[]):  
        data = {
            'authToken': self.__authToken,
            'zoneConfig': zoneConfig,
            'recordsToAdd': recordsToAdd,
            'recordsToDelete': recordsToDelete
        }        
        return getApiResponse(self.__baseUrl, '/api/dns/v1/json/zoneUpdate', data)

    # custom functions

    def getRecordsToDelete(self, recordName, recordType):
        filter = filters.getAndFilter([
            filters.getFilter("RecordName", recordName),
            filters.getFilter("RecordType", recordType)
        ])
        return self.getRecordsToDeleteByFilter(filter)

    def getRecordsToDeleteByFilter(self, filter):
        # query api for records matching this filter
        recordsResponse = self.recordFind(filter)
        return dns.getRecordsToDeleteFromResponse(recordsResponse)
    
    def updateRecord(self, recordName, recordType, newValue, ttl=None):

        # create filter to filter for objects of given name and type
        filter = filters.getAndFilter([
            filters.getFilter("RecordName", recordName),
            filters.getFilter("RecordType", recordType)
        ])

        # query for objects matching the filter
        recordsResponse = self.recordFind(filter)

        # stop if there are no matching objects or if they do not have a zoneConfigId
        if not recordsResponse['data'] or not recordsResponse['data'][0]['zoneConfigId']:
            raise ObjectNotFoundError("Could not find any existing records to update or atleast no zoneConfigId.")

        # reuse ttl if not explicitly given
        if not ttl:
            ttl = recordsResponse['data'][0]['ttl']

        # assuming that all entries exist within the same zoneConfig
        zoneConfig = dns.getZoneConfig(id=recordsResponse['data'][0]['zoneConfigId'])

        # prepare to remove all entries found earlier and add the new one
        recordsToDelete = dns.getRecordsToDeleteFromResponse(recordsResponse)
        recordsToAdd = [
            dns.getRecordToAddEntry(recordName, recordType, newValue, ttl),
        ]

        # only update if there is more than one entry or the current value does not match the given one
        if len(recordsToDelete) == 1 and recordsToDelete[0]['content'] == newValue:
            print('Not updating {0} current value for type {1} already matches the new value: {2}'.format(recordName, recordType, newValue))
            return

        # update the zone and signal the update by returning true
        return self.zoneUpdate(zoneConfig, recordsToAdd, recordsToDelete)

    def updateKnownRecord(self, zoneConfigName, recordName, recordType, newValue, oldValue, ttl=600):
        pass

    def addRecord(self, zoneConfigName, recordName, recordType, value, ttl=600):
        zoneConfig = { 'name': zoneConfigName }
        recordsToAdd = [
            dns.getRecordToAddEntry(recordName, recordType, value, ttl),
        ]
        return self.zoneUpdate(zoneConfig, recordsToAdd)
    
    def deleteRecords(self, zoneConfigName, recordName, recordType):
        zoneConfig = { 'name': zoneConfigName }
        recordsToDelete = self.getRecordsToDelete(recordName, recordType)
        
        # only call api if there are any items to delete
        if recordsToDelete and len(recordsToDelete) > 0:
            return self.zoneUpdate(zoneConfig, [], recordsToDelete)
