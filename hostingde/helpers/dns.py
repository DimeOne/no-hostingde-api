
def getZoneConfigFromZone(zone):
    if zone['zoneConfig']['name']:
        return { 'id': zone['zoneConfig']['name'] }
    return { 'name': zone['zoneConfig']['id'] }

def getZoneConfig(name=None, id=None):
    zoneConfig = {}
    if name:
        zoneConfig['name'] = name
    if id:
        zoneConfig['id'] = id
    return zoneConfig

def getRecordToAddEntry(name, type, content, ttl=8600):
    return {
        'name': name, 
        'type': type, 
        'content': content, 
        'ttl': ttl
    }

def getRecordsToDeleteEntries(records):
    recordsToDelete = []
    for record in records:
        recordsToDelete.append(getRecordToDeleteEntryFromRecord(record))
    return recordsToDelete

def getRecordToDeleteEntryFromRecord(record):
    return getRecordToDeleteEntry(record['name'], record['type'], record['content'])

def getRecordToDeleteEntry(name, type, content):
    return {
        'name': name, 
        'type': type, 
        'content': content
    }

def getRecordDomainList(recordName):
    parts = recordName.split(".")
    partCount = len(parts)
    domains = []

    for i in range(partCount, 1, -1):
        name = ".".join(parts[partCount - i:partCount])
        domains.append(name)
    
    return domains

def getBestZoneForRecord(zones, recordName, recordType=None, recordContent=None):
        if len(zones) == 0:
            return None
        if len(zones) == 1:
            return zones[0]
        # reorder zhe zones by path depth ( determined by dots )
        sortedZones = getZonesOrderedByDepth(zones)

        # return the first zone with a matching recordName [and recordType]
        for zone in sortedZones:
            if (zoneContainsRecord(zone, recordName, recordType, recordContent)):
                return zone
        
        # if no exact match has been found with recordContent, iterate again,
        # to search for a match without recordContent
        if recordContent:
            for zone in sortedZones:
                if (zoneContainsRecord(zone, recordName, recordType)):
                    return zone

        # if no exact match has been found without recordContent, iterate one last time, to check for a match based on name only
        # to search for a match without recordContent
        if recordContent:
            for zone in sortedZones:
                if (zoneContainsRecord(zone, recordName)):
                    return zone

        # return the deepest zone if none contains the given record
        return sortedZones[0]

def getZonesOrderedByDepth(zones):
    return sorted(zones, key=lambda x: (x['zoneConfig']['nameUnicode'].count(".")), reverse=True)

def zoneRecordMatches(record, recordName, recordType=None, recordContent=None):
    if (record['name'].lower() == recordName.lower() 
        and (recordType is None or record['type'].lower() == recordType.lower())
        and (recordContent is None or record['content'].lower() == recordContent.lower())):
        return True
    return False

def zoneContainsRecord(zone, recordName, recordType=None, recordContent=None):  
    for record in zone['records']:
        if zoneRecordMatches(record, recordName, recordType, recordContent):
            return True
    return False

def getMatchingRecordsFromZone(zone, recordName, recordType=None, recordContent=None):
    zoneRecords =  []
    for record in zone['records']:
        if zoneRecordMatches(record, recordName, recordType, recordContent):
            zoneRecords.append(record)
    return zoneRecords

def getZoneUpdateFromZone(zone, recordName, recordType, recordContent=None, oldContent=None, ttl=None):
    zoneConfig = getZoneConfigFromZone(zone)

    # check the zone for previous records that should be deleted
    previousRecords = getMatchingRecordsFromZone(zone, recordName, recordType, oldContent)
    recordsToDelete = getRecordsToDeleteEntries(previousRecords)

    if ttl is None and len(previousRecords) > 0:
        ttl = previousRecords[0]['ttl']

    if ttl is None:
        ttl = 8400

    recordsToAdd = []
    if recordContent:
        recordsToAdd = [getRecordToAddEntry(recordName, recordType, recordContent, ttl)] 

    return (zoneConfig, recordsToAdd, recordsToDelete)
