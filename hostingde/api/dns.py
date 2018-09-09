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

    # hosting.de api request helper functions

    def getCommonFilterBody(self, requestFilter, limit, page, sort):
        return {
            'authToken': self.__authToken,
            'filter': requestFilter,
            'limit': limit,
            'page': page,
            'sort': sort
        }

    def getZoneCreateBody(self, zoneConfig, records, useDefaultNameserverSet=False, nameserverSetId=None):
        data = {
            'authToken': self.__authToken,
            'zoneConfig': zoneConfig,
            'records': records,
            'useDefaultNameserverSet': useDefaultNameserverSet
        }
        if nameserverSetId:
            data['nameserverSetId'] = nameserverSetId
        return data

    def getZoneConfigBody(self, zoneConfigId=None, zoneConfigName=None):
        data = {}
        if zoneConfigId:
            data['zoneConfigId'] = zoneConfigId
        elif zoneConfigName:
            data['zoneConfigName'] = zoneConfigName
        return data

    def getZoneUpdateBody(self, zoneConfig, recordsToAdd, recordsToDelete=[]):
        return {
            'authToken': self.__authToken,
            'zoneConfig': zoneConfig,
            'recordsToAdd': recordsToAdd,
            'recordsToDelete': recordsToDelete
        }

    # hosting.de api list functions

    def recordsFind(self, recordFilter, limit=25, page=1, sort=None):
        """Hosting.de api function for listing records - https://www.hosting.de/api/#listing-records"""
        data = self.getCommonFilterBody(recordFilter, limit, page, sort)
        return getApiResponse(self.__baseUrl, '/api/dns/v1/json/recordsFind', data)

    def zoneConfigsFind(self, zoneConfigFilter, limit=25, page=1, sort=None):
        """Hosting.de api function for listing zone configs - https://www.hosting.de/api/#list-zoneconfigs"""
        data = self.getCommonFilterBody(zoneConfigFilter, limit, page, sort)
        return getApiResponse(self.__baseUrl, '/api/dns/v1/json/zoneConfigsFind', data)

    def zonesFind(self, zoneFilter, limit=25, page=1, sort=None):
        """Hosting.de api function for listing zones - https://www.hosting.de/api/#listing-zones"""        
        data = self.getCommonFilterBody(zoneFilter, limit, page, sort)
        return getApiResponse(self.__baseUrl, '/api/dns/v1/json/zonesFind', data)

    # hosting.de api zone editing functions

    def zoneCreate(self, zoneConfig, records, useDefaultNameserverSet=False, nameserverSetId=None):
        """Hosting.de api function for creating a zone - https://www.hosting.de/api/#creating-new-zones"""
        data = self.getZoneCreateBody(zoneConfig, records, useDefaultNameserverSet, nameserverSetId)
        return getApiResponse(self.__baseUrl, '/api/dns/v1/json/zoneCreate', data)

    def zoneDelete(self, zoneConfigId=None, zoneConfigName=None):
        """Hosting.de api function for deleting a zone - https://www.hosting.de/api/#deleting-zones"""
        data = self.getZoneConfigBody(zoneConfigId, zoneConfigName)
        return getApiResponse(self.__baseUrl, '/api/dns/v1/json/zoneRecreate', data)

    def zoneRecreate(self, zoneConfig, records, useDefaultNameserverSet=False, nameserverSetId=None):
        """Hosting.de api function for recreating a zone - https://www.hosting.de/api/#recreating-existing-zones"""
        data = self.getZoneCreateBody(zoneConfig, records, useDefaultNameserverSet, nameserverSetId)
        return getApiResponse(self.__baseUrl, '/api/dns/v1/json/zoneRecreate', data)

    def zoneUpdate(self, zoneConfig, recordsToAdd, recordsToDelete=[]):  
        """Hosting.de api function for updating a zone - https://www.hosting.de/api/#updating-zones"""
        data = self.getZoneUpdateBody(zoneConfig, recordsToAdd, recordsToDelete)
        return getApiResponse(self.__baseUrl, '/api/dns/v1/json/zoneUpdate', data)

    # custom api functions for information gathering

    def getZonesByFilter(self, zoneFilter, limit=25, page=1, sort=None):
        """Get zones by filter
        
        This function returnes a list of zone objects
        https://www.hosting.de/api/#the-zone-object
        """
        zoneResponse = self.zonesFind(zoneFilter, limit, page, sort)

        # stop if we cannot find a zone to update
        if zoneResponse['totalEntries'] == 0:
            raise ObjectNotFoundError("Could not find any zone matching the filter.")

        return zoneResponse['data']

    def getZonesByRecord(self, recordName, recordType=None, recordContent=None, limit=25, page=1, sort=None):
        """Get zones containing a given record
        Even though documentation for zonesFind api call does not mention record based filters, 
        these filters taken from recordsFind have been working during development.
        This behaviour may change in the future, breaking this function.

        This function returnes a list of zone objects
        https://www.hosting.de/api/#the-zone-object

        The zones returned by the api are by default ordered by name alphabetically, 
        the first zone might not be the best match.
        """
        zoneFilter = filters.getRecordFilter(recordName, recordType, recordContent)
        return self.getZonesByFilter(zoneFilter, limit, page, sort)

    def getZonesByDomainHierarchy(self, recordName, limit=25, page=1, sort=None):
        """Get zones based on domain hierarchy
        If we do not know of an existing record, we need to search for all zones based on domain hierarchy, 
        this can be much information and should be avoided with huge or many zones as performance will suffer
        
        Zones are searched as:
        e.g. "test.demo.example.org" -> ["test.demo.example.org", "demo.example.org", "example.org"]
        
        This function returnes a list of zone objects
        https://www.hosting.de/api/#the-zone-object

        The zones returned by the api are ordered by name alphabetically, instead of domain hierarchy depth,
        the first zone might not be the best match.
        """
        domains = dns.getRecordDomainList(recordName)
        zoneFilter = filters.getZoneDomainListFilter(domains)
        return self.getZonesByFilter(zoneFilter, limit, page, sort)
  
    def getZoneByRecord(self, recordName, recordType=None, recordContent=None, limit=25, page=1):
        """Get best matching zone for existing record
        This function queries the api for existing zones based on the given record properties.

        This function returnes the best matching zone objects for the given record
        https://www.hosting.de/api/#the-zone-object
        """
        zones = self.getZonesByRecord(recordName, recordType, recordContent, limit, page)
        recordZone = dns.getBestZoneForRecord(zones, recordName, recordType)

        return recordZone

    def getZoneByDomain(self, recordName, recordType=None, recordContent=None, limit=25, page=1):
        """Get best matching zone for a record based on domain hierarchy
        If we do not know of an existing record, we need to search for all zones based on domain hierarchy, 
        this can be much information and should be avoided with huge or many zones as performance will suffer

        This function returnes the best matching zone objects for the given record
        https://www.hosting.de/api/#the-zone-object
        """
        zones = self.getZonesByDomainHierarchy(recordName, limit, page)
        recordZone = dns.getBestZoneForRecord(zones, recordName, recordType, recordContent)

        return recordZone

    def getRecordsByFilter(self, recordFilter, limit=50, page=1, sort=None):
        recordsResponse = self.recordsFind(recordFilter, limit, page, sort)

        # stop if we cannot find a zone to update
        if recordsResponse['totalEntries'] == 0:
            raise ObjectNotFoundError("Could not find any records matching the filter.")

        return recordsResponse['data']

    def getRecords(self, recordName, recordType=None, recordContent=None, limit=50, page=1, sort=None):
        """Get records based on given record

        This function returnes a list of record objects
        https://www.hosting.de/api/#the-record-object
        """
        recordFilter = filters.getRecordFilter(recordName, recordType, recordContent)
        return  self.getRecordsByFilter(recordFilter, limit, page, sort)

    # custom api functions that require more information but do not require information from  api - single api call

    def addZoneRecordEntry(self, zoneConfig, recordName, recordType, recordContent, ttl=600):
        """Adds a new record to a known zone."""
        recordsToAdd = [
            dns.getRecordToAddEntry(recordName, recordType, recordContent, ttl),
        ]
        return self.zoneUpdate(zoneConfig, recordsToAdd)

    def deleteZoneRecordEntry(self, zoneConfig, recordName, recordType, recordContent):
        """Delete a known record in a known zone."""
        recordToDelete = [
            dns.getRecordToDeleteEntry(recordName, recordType, recordContent)
        ]
        return self.zoneUpdate(zoneConfig, [], recordToDelete)

    def updateZoneRecordEntry(self, zoneConfig, recordName, recordType, recordContent, oldContent, ttl=600):
        """Change a known record in a known zone."""
        recordToDelete = [
            dns.getRecordToDeleteEntry(recordName, recordType, oldContent)
        ]
        recordsToAdd = [
            dns.getRecordToAddEntry(recordName, recordType, recordContent, ttl),
        ]
        return self.zoneUpdate(zoneConfig, recordsToAdd, recordToDelete)

    # custom api functions that require more information but still require some information from api - less zones to query and iterate

    def deleteZoneRecordEntries(self, zoneFilter, recordName, recordType, recordContent=None):
        """Delete existing records in a known zone based on a filter."""
        recordZones = self.getZonesByFilter(zoneFilter)
        recordZone = dns.getBestZoneForRecord(recordZones, recordName, recordType, recordContent)        
        zoneConfig, recordsToAdd, recordsToDelete = dns.getZoneUpdateFromZone(recordZone, recordName, recordType, None, recordContent)
        return self.zoneUpdate(zoneConfig, recordsToAdd, recordsToDelete)

    def setZoneRecordEntry(self, zoneFilter, recordName, recordType, recordContent, oldContent=None, ttl=None):
        """Set records in a known zone based on a filter. Matching previous records are deleted."""
        recordZones = self.getZonesByFilter(zoneFilter)
        recordZone = dns.getBestZoneForRecord(recordZones, recordName, recordType, oldContent)        
        zoneConfig, recordsToAdd, recordsToDelete = dns.getZoneUpdateFromZone(recordZone, recordName, recordType, recordContent, oldContent, ttl)
        return self.zoneUpdate(zoneConfig, recordsToAdd, recordsToDelete)

    # custom api functions for easy use without knowning zoneConfig
    # these functions query for zone information from api
    # this can lead to performance issues with many or large zones

    def addRecordEntry(self, recordName, recordType, recordContent, ttl=600):
        """Add a record to an unknown zone."""
        recordZone = self.getZoneByDomain(recordName, recordType)
        zoneConfig = dns.getZoneConfigFromZone(recordZone)
        recordsToAdd = [dns.getRecordToAddEntry(recordName, recordType, recordContent, ttl)]
        return self.zoneUpdate(zoneConfig, recordsToAdd)

    def deleteRecordEntry(self, recordName, recordType, recordContent=None):
        """Delete existing records in an unknown zone."""
        recordZone = self.getZoneByRecord(recordName, recordType, recordContent)       
        zoneConfig, recordsToAdd, recordsToDelete = dns.getZoneUpdateFromZone(recordZone, recordName, recordType, None, recordContent)
        return self.zoneUpdate(zoneConfig, recordsToAdd, recordsToDelete)
   
    def setRecordEntry(self, recordName, recordType, recordContent, oldContent=None, ttl=None):
        """Set or create a record in an unknown zone. Matching previous records are deleted."""
        recordZone = self.getZoneByDomain(recordName, recordType, oldContent)
        zoneConfig, recordsToAdd, recordsToDelete = dns.getZoneUpdateFromZone(recordZone, recordName, recordType, recordContent, oldContent, ttl)
        return self.zoneUpdate(zoneConfig, recordsToAdd, recordsToDelete)

    def updateRecordEntry(self, recordName, recordType, recordContent, oldContent=None, ttl=None):
        """Update an existing record in an unknown zone. Matching previous records are deleted."""
        recordZone = self.getZoneByRecord(recordName, recordType, oldContent)
        zoneConfig, recordsToAdd, recordsToDelete = dns.getZoneUpdateFromZone(recordZone, recordName, recordType, recordContent, oldContent, ttl)
        return self.zoneUpdate(zoneConfig, recordsToAdd, recordsToDelete)
