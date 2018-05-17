
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

def getRecordsToDeleteFromResponse(response):
    recordsToDelete = []
    for item in response['data']:
        recordsToDelete.append(getRecordToDeleteEntryFromResponseItem(item))

    return recordsToDelete

def getRecordToDeleteEntryFromResponseItem(item):
    return getRecordToDeleteEntry(item['name'], item['type'], item['content'])

def getRecordToDeleteEntry(name, type, content):
    return {
        'name': name, 
        'type': type, 
        'content': content
    }
