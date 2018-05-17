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

The only API functions that I have implemented so far are:

- recordFind(filter, limit=25, page=1, sort=None) --> [listing-records]
- zoneFind(filter, limit=25, page=1, sort=None) --> [listing-zones]
- zoneUpdate(zoneConfig, recordsToAdd, recordsToDelete=[]) --> [updating-zones]

There are also helpers to aid with correct data structes for these functions

### Custom functions

In addition to the API functions provided by hosting.de, I added some functions for common simple use cases.
These functions are useful for operations that only affect a single hostname and record type.

#### Single API call

- addRecord(self, zoneConfigName, recordName, recordType, value, ttl=600)
- updateKnownRecord(self, zoneConfigName, recordName, recordType, newValue, oldValue, ttl=600)
- getRecordsToDelete(self, recordName, recordType)
- getRecordsToDeleteByFilter(self, filter)

#### Multiple API calls (Lookup values first)

- deleteRecords(self, zoneConfigName, recordName, recordType)
- updateRecord(self, recordName, recordType, newValue, ttl=None)

## Known Issues

- No warning handling from responses

## Dependencies

- requests
- urllib3

## Install

### Easy

```sh
pip install no-hostingde-api
```

### Developer

```sh
git clone https://github.com/DimeOne/hostingde-api.git
cd hostingde-api
python setup.py develop
```

## Examples

Adding IPv4 IP:

```python
from hostingde.api.dns import DnsApiClient
client = DnsApiClient("MySecretLongApiKey")
client.AddRecord("dev.example.org", "demo.dev.example.org", "A", "127.0.0.1", ttl=8400)
```

Adding IPv6 IP:

```python
from hostingde.api.dns import DnsApiClient
client = DnsApiClient("MySecretLongApiKey")
client.AddRecord("dev.example.org", "demo.dev.example.org", "AAAA", "AFFE::1", ttl=8400)
```

Update IPv4 IP:

```python
from hostingde.api.dns import DnsApiClient
client = DnsApiClient("MySecretLongApiKey")
client.UpdateRecord("demo.dev.example.org", "A", "AFFE::1")
```

In this case the zoneConfigName and TTL are used from the first previous record, ttl can be specified. Value is only updated if there is more than one record or the current value differs from the new value.

## Build

```sh
python setup.py sdist
python setup.py bdist_wheel
```

## References

- [Hosting.de API Reference]
  - [listing-records]
  - [listing-zones]
  - [updating-zones]

 [Hosting.de API Reference]: https://www.hosting.de/api/
 [listing-records]: https://www.hosting.de/api/#listing-records
 [listing-zones]: https://www.hosting.de/api/#listing-zones
 [updating-zones]: https://www.hosting.de/api/#updating-zones