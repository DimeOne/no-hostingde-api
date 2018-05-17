
def getOrFilter(subFilters):
    return {
        'subFilterConnective': 'OR', 
        'subFilter': subFilters
    }

def getAndFilter(subFilters):
    return {
        'subFilterConnective': 'AND', 
        'subFilter': subFilters
    }

def getFilter(field, value, relation=None):
    if relation:
        return {
            'field': field, 
            'value': value, 
            'relation': relation
        }
    return {
        'field': field, 
        'value': value
    }
