# Unofficial Hosting.de API Client

Python3 library for accessing the hosting.de dns api.

[![PyPI version](https://badge.fury.io/py/no-hostingde-api.svg)](https://badge.fury.io/py/no-hostingde-api)

## Disclaimer

This is a very basic unofficial client for the hosting.de API. I have only implemented very few functions that I need for another hobby project. I am not in any way connected to hosting.de other then being a paying customer.

I'd be happy to give up this library for an official and supported library.

I have built this library to use it for ddns scripts and let's encrypt wildcard certificate requests.

Validation and sanitizing of any inputs is expected to be done at higher level.

**USE THIS LIBRARY AT YOUR OWN RISK, DO NOT USE IN PRODUCTION. DO NOT EXPECT SUPPORT.**

## DNS

I have only implemented functions and data structures for the DNS API.

### API functions

The Hosting.de DNS API functions that I have implemented so far are:

- recordsFind(recordFilter, limit=25, page=1, sort=None)
- zoneConfigsFind(zoneConfigFilter, limit=25, page=1, sort=None)
- zonesFind(zoneFilter, limit=25, page=1, sort=None)
- zoneCreate(zoneConfig, records, useDefaultNameserverSet=False, nameserverSetId=None)
- zoneDelete(zoneConfigId=None, zoneConfigName=None)
- zoneRecreate(zoneConfig, records, useDefaultNameserverSet=False, nameserverSetId=None)
- zoneUpdate(zoneConfig, recordsToAdd, recordsToDelete=[])

There are also helpers to aid with correct data structes for these functions and helper functions, that require less information.

### Custom API functions

- getZonesByFilter(zoneFilter, limit=25, page=1, sort=None)
- getZonesByRecord(recordName, recordType=None, recordContent=None, limit=25, page=1, sort=None)
- getZonesByDomainHierarchy(recordName, limit=25, page=1, sort=None)
- getZoneByRecord(recordName, recordType=None, recordContent=None, limit=25, page=1)
- getZoneByDomain(recordName, recordType=None, recordContent=None, limit=25, page=1)
- getRecordsByFilter(recordFilter, limit=50, page=1, sort=None)
- getRecords(recordName, recordType=None, recordContent=None, limit=50, page=1, sort=None)

- addZoneRecordWithConfig(zoneConfig, recordName, recordType, recordContent, ttl=600)
- deleteZoneRecordWithConfig(zoneConfig, recordName, recordType, recordContent)
- updateZoneRecordWithConfig(zoneConfig, recordName, recordType, recordContent, oldContent, ttl=600)

- deleteZoneRecordsWithFilter(zoneFilter, recordName, recordType, recordContent=None)
- setZoneRecordWithFilter(zoneFilter, recordName, recordType, recordContent, oldContent=None, ttl=600)

- addZoneRecord(zoneName, recordName, recordType, recordContent, ttl=600)
- deleteZoneRecord(zoneName, recordName, recordType, recordContent)
- updateZoneRecord(zoneName, recordName, recordType, recordContent, oldContent, ttl=600)
- deleteZoneRecords(zoneName, recordName, recordType, recordContent=None)
- setZoneRecord(zoneName, recordName, recordType, recordContent, oldContent=None, ttl=600)

- addRecord(recordName, recordType, recordContent, ttl=600)
- deleteRecord(recordName, recordType, recordContent=None)
- setRecord(recordName, recordType, recordContent, oldContent=None, ttl=600)
- updateRecord(recordName, recordType, recordContent, oldContent=None, ttl=600)

## Known Issues

- No warning handling from responses

## Dependencies

- requests

## Install

### Easy

```sh
pip install no-hostingde-api
```

### Developer

```sh
git clone https://github.com/DimeOne/no-hostingde-api.git
cd hostingde-api
python setup.py develop
```

## References

- [Github Project Page]
- [Hosting.de Provider]
- [Hosting.de API Reference]
- [Hosting.de DNS API Reference]

[Hosting.de Provider]: https://www.hosting.de
[Github Project Page]: https://github.com/DimeOne/no-hostingde-api
[Hosting.de API Reference]: https://www.hosting.de/api/
[Hosting.de DNS API Reference]: https://www.hosting.de/api/#dns