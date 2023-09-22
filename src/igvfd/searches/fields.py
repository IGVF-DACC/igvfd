from snosearch.fields import ResponseField
from snovault import TYPES
from collections import OrderedDict
from snovault.elasticsearch.searches.interfaces import SEARCH_CONFIG


class ResultColumnsResponseField(ResponseField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, *args, **kwargs):
        self.parent = kwargs.get('parent')
        request = self.get_request()
        facets = self.parent.response.get('facets', [])
        columns = self.parent.response.get('columns', [])
        return {
            'result_columns': get_result_columns(request, facets, columns)
        }

# only return the columns of the concrete types if the type is returned in search restult


def get_result_columns(request, facets, report_response_columns):
    columns = OrderedDict({'@id': {'title': 'ID'}})
    configs = request.params.getall('config')
    # if config in query string
    if configs:
        columns.update(report_response_columns)

    else:
        abstract_types = get_abstract_types(request)
        types_in_search_result = []
        for facet in facets:
            if facet['field'] == 'type':
                for term in facet['terms']:
                    type_name = term['key']
                    if type_name not in abstract_types:
                        types_in_search_result.append(term['key'])
                break
        for type_str in types_in_search_result:
            schema = request.registry[TYPES][type_str].schema
            search_config = request.registry[SEARCH_CONFIG].as_dict()[type_str]

            if 'columns' in search_config:
                columns.update(search_config['columns'])
            else:
                # default columns if not explicitly specified
                columns.update(OrderedDict(
                    (name, {
                        'title': schema['properties'][name].get('title', name)
                    })
                    for name in [
                        '@id', 'title', 'description', 'name', 'accession',
                        'aliases'
                    ] if name in schema['properties']
                ))
    fields_requested = request.params.getall('field')
    # if field in query string
    if fields_requested:
        limited_columns = OrderedDict()
        for field in fields_requested:
            if field in columns:
                limited_columns[field] = columns[field]
            else:
                # We don't currently traverse to other schemas for embedded
                # objects to find property titles. In this case we'll just
                # show the field's dotted path for now.
                limited_columns[field] = {'title': field}
                for type_str in types_in_search_result:
                    schema = request.registry[TYPES][type_str].schema
                    if field in schema['properties']:
                        limited_columns[field] = {
                            'title': schema['properties'][field]['title']
                        }
                        break
        columns = limited_columns
    return columns


def get_abstract_types(request):
    types = []
    item_registry = request.registry[TYPES]
    for name, item in item_registry.abstract.items():
        subtypes = item.subtypes
        if len(subtypes) > 1:
            types.append(name)
    return types
