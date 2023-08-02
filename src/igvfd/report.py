from collections import OrderedDict
from pyramid.compat import bytes_
from pyramid.view import view_config
from snovault import TYPES
from snovault.elasticsearch.searches.interfaces import SEARCH_CONFIG
from snosearch.responses import FieldedResponse
from snosearch.fields import ColumnsResponseField
from snosearch.fields import MultipleTypesReportWithFacetsResponseField
from snosearch.parsers import ParamsParser
from igvfd.search_views import search_generator
from igvfd.searches.defaults import DEFAULT_ITEM_TYPES
from igvfd.searches.defaults import RESERVED_KEYS


import datetime
import re


def includeme(config):
    config.add_route('report_download', '/report.tsv')
    config.scan(__name__)


def lookup_column_value(value, path):
    nodes = [value]
    names = path.split('.')
    for name in names:
        nextnodes = []
        for node in nodes:
            if name not in node:
                continue
            value = node[name]
            if isinstance(value, list):
                nextnodes.extend(value)
            else:
                nextnodes.append(value)
        nodes = nextnodes
        if not nodes:
            return ''
    # if we ended with an embedded object, show the @id
    if nodes and hasattr(nodes[0], '__contains__') and '@id' in nodes[0]:
        nodes = [node['@id'] for node in nodes]
    deduped_nodes = []
    for n in nodes:
        if isinstance(n, dict):
            n = str(n)
        if n not in deduped_nodes:
            deduped_nodes.append(n)
    return u','.join(u'{}'.format(n) for n in deduped_nodes)


def format_row(columns):
    """Format a list of text columns as a tab-separated byte string."""
    return b'\t'.join([bytes_(' '.join(c.strip('\t\n\r').split()), 'utf-8') for c in columns]) + b'\r\n'


def _convert_camel_to_snake(type_str):
    tmp = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', type_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', tmp).lower()


@view_config(route_name='report_download', request_method='GET')
def report_download(context, request):
    downloadtime = datetime.datetime.now()
    request.GET['limit'] = '0'
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            MultipleTypesReportWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            ),
            ColumnsResponseField(),

        ]
    )
    response = fr.render()
    facets = response.json['facets']
    abstract_types = get_abstract_types(request)
    types_in_search_result = []
    for facet in facets:
        if facet['field'] == 'type':
            for term in facet['terms']:
                type_name = term['key']
                if type_name not in abstract_types:
                    types_in_search_result.append(term['key'])
            break
    types_str = ''.join(request.params.getall('type'))
    snake_types_str = _convert_camel_to_snake(types_str).replace("'", '')
    # Make sure we get all results
    request.GET['limit'] = 'all'
    results = search_generator(request)
    columns = list_visible_columns_for_schemas(request, types_in_search_result, response.json['columns'])

    def format_header(seq):
        newheader = '%s\t%s%s?%s\r\n' % (downloadtime, request.host_url, '/report/', request.query_string)
        return(bytes(newheader, 'utf-8'))

    # Work around Excel bug; can't open single column TSV with 'ID' header
    if len(columns) == 1 and '@id' in columns:
        columns['@id']['title'] = 'id'

    header = [column.get('title') or field for field, column in columns.items()]

    def generate_rows():
        yield format_header(header)
        yield format_row(header)
        for item in results['@graph']:
            values = [lookup_column_value(item, path) for path in columns]
            yield format_row(values)

    # Stream response using chunked encoding.
    request.response.content_type = 'text/tsv'
    request.response.content_disposition = 'attachment;filename="{}_report_{}_{}_{}_{}h_{}m.tsv"'.format(
        snake_types_str,
        downloadtime.year,
        downloadtime.month,
        downloadtime.day,
        downloadtime.hour,
        downloadtime.minute
    )
    request.response.app_iter = generate_rows()
    return request.response


def list_visible_columns_for_schemas(request, types, report_response_columns):
    """
    Returns mapping of default columns for a set of types.
    """
    columns = OrderedDict({'@id': {'title': 'ID'}})
    configs = request.params.getall('config')
    if configs:
        columns.update(report_response_columns)
    else:
        for type_str in types:
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
                for type_str in types:
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
