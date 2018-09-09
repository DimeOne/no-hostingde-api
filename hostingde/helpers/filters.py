def getOrFilter(subFilters):
    return {"subFilterConnective": "OR", "subFilter": subFilters}


def getOrFilters(**kwArgs):
    return getOrFilter(getFilters(**kwArgs))


def getAndFilter(subFilters):
    return {"subFilterConnective": "AND", "subFilter": subFilters}


def getAndFilters(**kwArgs):
    return getAndFilter(getFilters(**kwArgs))


def getFilters(**kwArgs):
    filters = []
    for key, value in kwArgs.items():
        filters.append(getFilter(key, value))
    return filters


def getFilter(field, value, relation=None):
    if relation:
        return {"field": field, "value": value, "relation": relation}
    return {"field": field, "value": value}


def getRecordFilter(recordName, recordType=None, recordContent=None):
    recordFilters = [getFilter("RecordName", recordName)]
    if recordType:
        recordFilters.append(getFilter("RecordType", recordType))
    if recordContent:
        recordFilters.append(getFilter("RecordContent", recordContent))
    return getAndFilter(recordFilters)


def getZoneDomainListFilter(domains):
    filters = []
    for domain in domains:
        filters.append(getFilter("ZoneNameUnicode", domain))
    return getOrFilter(filters)
