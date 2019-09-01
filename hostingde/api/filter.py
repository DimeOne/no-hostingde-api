class BaseFilter:
    def __init__(self):
        pass

    def get_filter_data(self):
        return {}

    def __str__(self):
        return self.get_filter_data().__str__()

    def __repr__(self):
        return self.__str__()

    def and_filter(self, field, value, relation=None):
        return AndFilter([self, Filter(field, value, relation)])

    def and_filter_obj(self, filter):
        return AndFilter([self, filter])

    def and_filters(self, filters):
        return AndFilter([self] + filters)

    def or_filter(self, field, value, relation=None):
        return OrFilter([self, Filter(field, value, relation)])

    def or_filter_obj(self, filter):
        return OrFilter([self, filter])

    def or_filters(self, filters):
        return OrFilter([self] + filters)


class Filter(BaseFilter):
    def __init__(self, field, value, relation=None):
        self.field = field
        self.value = value
        self.relation = relation

    def get_filter_data(self):
        if self.relation:
            return {"field": self.field, "value": self.value, "relation": self.relation}
        return {"field": self.field, "value": self.value}


class BaseFilterConnection(BaseFilter):
    def __init__(self, connection, filters=[]):
        self.connection = connection
        self.sub_filters = filters

    def get_filter_data(self):
        if len(self.sub_filters) == 1:
            return self.sub_filters[0].get_filter_data()
        elif len(self.sub_filters) == 0:
            return {}
        else:
            sub_filter_data = []
            for sub_filter in self.sub_filters:
                sub_filter_data.append(sub_filter.get_filter_data())

            return {
                "subFilterConnective": self.connection,
                "subFilter": sub_filter_data,
            }


class OrFilter(BaseFilterConnection):
    def __init__(self, filters=[]):
        self.connection = "OR"
        self.sub_filters = filters

    def or_filter(self, field, value, relation=None):
        self.sub_filters.append(Filter(field, value, relation))
        return self

    def or_filter_obj(self, filter):
        self.sub_filters.append(filter)
        return self

    def or_filters(self, filters):
        self.sub_filters += filters
        return self


class AndFilter(BaseFilterConnection):
    def __init__(self, filters=[]):
        self.connection = "AND"
        self.sub_filters = filters

    def and_filter(self, field, value, relation=None):
        self.sub_filters.append(Filter(field, value, relation))
        return self

    def and_filter_obj(self, filter):
        self.sub_filters.append(filter)
        return self

    def and_filters(self, filters):
        self.sub_filters += filters
        return self
