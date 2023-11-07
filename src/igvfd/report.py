from collections import OrderedDict
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import view_config
from snovault import TYPES
from snovault.elasticsearch.searches.interfaces import SEARCH_CONFIG
from snosearch.parsers import QueryString
from snovault.compat import bytes_
from igvfd.searches.generator import search_generator

import datetime
import re

# Those columns contain href value
HREF_COLUMN_KEYS = ['href', 'attachment', 'attachment.href']


def includeme(config):
    config.add_route('report_download', '/report.tsv')
    config.add_route('multitype_report_download', '/multireport.tsv')
    config.scan(__name__, categories=None)


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


def format_row_full_url(columns, href_index, host_url, id):
    """Format a list of text columns as a tab-separated byte string. add host_url to href to form a full length url"""
    row = []
    for index, column in enumerate(columns):
        ls = column.strip('\t\n\r').split()
        if index == href_index:
            # href is not embedded, append host_url directly
            if len(ls) == 1:
                # attachment.href
                if ls[0].startswith('@@download'):
                    ls[0] = host_url + id + ls[0]
                # href from File
                else:
                    ls[0] = host_url + ls[0]
            # href is embedded
            else:
                for index, item in enumerate(ls):
                    if ''.join([i for i in item if i.isalpha()]) == 'href':
                        embedded_index = index + 1
                        break
                if embedded_index:
                    ls[embedded_index] = ls[embedded_index][0] + host_url + id + ls[embedded_index][1:]

        row.append(bytes_(' '.join(ls), 'utf-8'))
    return b'\t'.join(row) + b'\r\n'


def _convert_camel_to_snake(type_str):
    tmp = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', type_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', tmp).lower()


@view_config(route_name='report_download', request_method='GET')
def report_download(context, request):
    downloadtime = datetime.datetime.now()

    types = request.params.getall('type')
    if len(types) != 1:
        msg = 'Report view requires specifying a single type.'
        raise HTTPBadRequest(explanation=msg)

    # Make sure we get all results
    request.GET['limit'] = 'all'
    type_str = types[0]
    schema = request.registry[TYPES][type_str].schema
    search_config = request.registry[SEARCH_CONFIG].as_dict()[type_str]
    columns = list_visible_columns_for_schemas(request, schema, search_config)
    snake_type = _convert_camel_to_snake(type_str).replace("'", '')
    results = search_generator(request)

    def format_header():
        newheader = '%s\t%s%s?%s\r\n' % (downloadtime, request.host_url, '/report/', request.query_string)
        return(bytes(newheader, 'utf-8'))

    # Work around Excel bug; can't open single column TSV with 'ID' header
    if len(columns) == 1 and '@id' in columns:
        columns['@id']['title'] = 'id'

    header = [column.get('title') or field for field, column in columns.items()]

    def generate_rows():
        yield format_header()
        yield format_row(header)
        for item in results['@graph']:
            values = [lookup_column_value(item, path) for path in columns]
            yield format_row(values)

    # Stream response using chunked encoding.
    request.response.content_type = 'text/tsv'
    request.response.content_disposition = 'attachment;filename="{}_report_{}_{}_{}_{}h_{}m.tsv"'.format(
        snake_type,
        downloadtime.year,
        downloadtime.month,
        downloadtime.day,
        downloadtime.hour,
        downloadtime.minute
    )
    request.response.app_iter = generate_rows()
    return request.response


def list_visible_columns_for_schemas(request, schema, search_config):
    """
    Returns mapping of default columns for a set of schemas.
    """
    columns = OrderedDict({'@id': {'title': 'ID'}})
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
                if field in schema['properties']:
                    limited_columns[field] = {
                        'title': schema['properties'][field]['title']
                    }
        columns = limited_columns
    return columns


@view_config(route_name='multitype_report_download', request_method='GET')
def multitype_report_download(context, request):
    downloadtime = datetime.datetime.now()
    qs = QueryString(request)
    qs.drop('limit')
    qs.append(('limit', '0'))
    query_string = qs.get_query_string()
    response = request.embed(f'/multireport?{query_string}')
    facets = response['facets']
    columns = response['result_columns']
    abstract_types = get_abstract_types(request)
    types_in_search_result = []
    for facet in facets:
        if facet['field'] == 'type':
            for term in facet['terms']:
                type_name = term['key']
                if type_name not in abstract_types:
                    types_in_search_result.append(term['key'])
            break
    report_type = 'mixed'
    if len(types_in_search_result) == 1:
        report_type = _convert_camel_to_snake(types_in_search_result[0]).replace("'", '')

    # Make sure we get all results
    request.GET['limit'] = 'all'
    results = search_generator(request)

    def format_header():
        newheader = '%s\t%s%s?%s\r\n' % (downloadtime, request.host_url, '/multireport/', request.query_string)
        return(bytes(newheader, 'utf-8'))

    # Work around Excel bug; can't open single column TSV with 'ID' header
    if len(columns) == 1 and '@id' in columns:
        columns['@id']['title'] = 'id'

    header_row = [column.get('title') or field for field, column in columns.items()]
    columns_keys = list(columns.keys())
    href_index = -1
    for index, item in enumerate(columns_keys):
        if item in HREF_COLUMN_KEYS:
            href_index = index

    def generate_rows():
        yield format_header()
        yield format_row(header_row)
        for item in results['@graph']:
            values = [lookup_column_value(item, path) for path in columns]
            yield format_row_full_url(values, href_index, request.host_url)

    # Stream response using chunked encoding.
    request.response.content_type = 'text/tsv'
    request.response.content_disposition = 'attachment;filename="igvf_{}_report_{}_{}_{}_{}h_{}m.tsv"'.format(
        report_type,
        downloadtime.year,
        downloadtime.month,
        downloadtime.day,
        downloadtime.hour,
        downloadtime.minute
    )
    request.response.app_iter = generate_rows()
    return request.response

# only return the columns of the concrete types if the type is returned in search restult


def get_result_columns(request, facets, report_response_columns):
    columns = OrderedDict({'@id': {'title': 'ID'}})
    configs = request.params.getall('config')
    abstract_types = get_abstract_types(request)
    types_in_search_result = []
    for facet in facets:
        if facet['field'] == 'type':
            for term in facet['terms']:
                type_name = term['key']
                if type_name not in abstract_types:
                    types_in_search_result.append(term['key'])
            break
    # if config in query string
    if configs:
        columns.update(report_response_columns)

    else:
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
