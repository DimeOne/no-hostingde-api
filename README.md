# Unofficial Hosting.de API Client and Certbot DNS Auth Plugin

Python3 library for accessing the hosting.de dns api.

[![PyPI version](https://badge.fury.io/py/no-hostingde-api.svg)](https://badge.fury.io/py/no-hostingde-api)

## Disclaimer

This is an unofficial client for the hosting.de API. I have only implemented very few functions that I need for another hobby project. I am not in any way connected to hosting.de other then being a paying customer.

I'd be happy to give up this library for an official and supported library.

I have built this library to use it for ddns scripts and let's encrypt wildcard certificate requests.

Validation and sanitizing of any inputs is expected to be done at higher level.

**USE THIS LIBRARY AT YOUR OWN RISK, DO NOT USE IN PRODUCTION. DO NOT EXPECT SUPPORT.**

## Features

- certbot dns authenticator plugin
- implemented all hosting.de api zone and record functions
- retry on busy api objects
- custom dns api helper functions
- dns api filter helpers
- dns api helpers

## Certbot DNS Authenticator Plugin

Introduced in version 0.3.0, this certbot dns authenticator plugin allows certificates
to be requested from letsencrypt for domains hosted by hosting.de.

This allows to create certificates for hosts that may not be reachable for webroot authentication,
or that require dns validation. e.g.: internal servers with private dns, wildcard certificates.

### Configuration

- credentials (path to ini file containing apikey)
- propagation-seconds (delay between dns record creation and validation) [default: 60]

**credentials.ini:**

```ini credentials.ini
no_hostingde_api:dns_hostingde_apikey=MY_SECRET_API_KEY_FOR_HOSTING_DE
```

This is the api key configured at [hosting.de profile] - the api key needs only the permissions to list and edit zones. ( DNS_ZONES_LIST & DNS_ZONES_EDIT )

### Install

```sh
pip install certbot no-hostingde-api
```

### Usage

After installation and creating the ini file containing the credentials,
the following command can be used to request a certificate using this plugin.

```sh
certbot certonly \
    -a no-hostingde-api:dns-hostingde \
    --no-hostingde-api:dns-hostingde-credentials ~/credentials.ini \
    --no-hostingde-api:dns-hostingde-propagation-seconds 60 \
    -d demo.example.org
```

## DNS Api Client

So far, only functions for zones, records and zoneConfigs have been implemented.
Some functions have been implemented, to allow easier usage of the api for single records,
that will query more or less information from the api.

The DnsApiClient has a builtin retry for busy api objects, by default 2s delay and 2 retries.

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

### Examples

Adding IPv4 IP:

```python
from hostingde.api.dns import DnsApiClient
client = DnsApiClient("MySecretLongApiKey")
# only 1 api call because we know the zone name:
client.AddZoneRecord("dev.example.org", "demo.dev.example.org", "A", "127.0.0.1", ttl=8400)
# alternative for unknown zone - requires 2 api calls, because we need to find the zone first - expensive!
client.AddRecord("demo.dev.example.org", "A", "127.0.0.1", ttl=8400)
```

Adding IPv6 IP:

```python
from hostingde.api.dns import DnsApiClient
client = DnsApiClient("MySecretLongApiKey")
client.AddZoneRecord("dev.example.org", "demo.dev.example.org", "AAAA", "AFFE::1", ttl=8400)
```

Update IPv4 IP:

```python
from hostingde.api.dns import DnsApiClient
client = DnsApiClient("MySecretLongApiKey")
client.UpdateRecord("demo.dev.example.org", "A", "128.0.0.1", "127.0.0.1", 60)
```

In this case the zoneConfigName and TTL are used from the first previous record, ttl can be specified. Value is only updated if there is more than one record or the current value differs from the new value.

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

or

```sh
git clone https://github.com/DimeOne/no-hostingde-api.git
cd hostingde-api
pip install -e .
```

## Build

```sh
python setup.py sdist bdist_wheel
```

## References

- [Github Project Page]
- [Hosting.de Provider]
- [Hosting.de Profile]
- [Hosting.de API Reference]
- [Hosting.de DNS API Reference]

[Hosting.de Provider]: https://www.hosting.de
[Hosting.de Profile]: https://secure.hosting.de/profile
[Github Project Page]: https://github.com/DimeOne/no-hostingde-api
[Hosting.de API Reference]: https://www.hosting.de/api/
[Hosting.de DNS API Reference]: https://www.hosting.de/api/#dns