from pyramid.view import view_config
from igvfd.searches.defaults import DEFAULT_ITEM_TYPES
from igvfd.searches.defaults import RESERVED_KEYS
from igvfd.searches.defaults import TOP_HITS_ITEM_TYPES
from igvfd.searches.fields import ResultColumnsResponseField
from snosearch.interfaces import AUDIT_TITLE
from snosearch.interfaces import MATRIX_TITLE
from snosearch.interfaces import REPORT_TITLE
from snosearch.interfaces import SEARCH_TITLE
from snosearch.interfaces import SUMMARY_MATRIX
from snosearch.interfaces import SUMMARY_TITLE
from snosearch.fields import AuditMatrixWithFacetsResponseField
from snosearch.fields import AllResponseField
from snosearch.fields import BasicSearchResponseField
from snosearch.fields import BasicMatrixWithFacetsResponseField
from snosearch.fields import MissingMatrixWithFacetsResponseField
from snosearch.fields import BasicSearchWithFacetsResponseField
from snosearch.fields import BasicReportWithFacetsResponseField
from snosearch.fields import MultipleTypesReportWithFacetsResponseField
from snosearch.fields import ClearFiltersResponseField
from snosearch.fields import ColumnsResponseField
from snosearch.fields import ContextResponseField
from snosearch.fields import DebugQueryResponseField
from snosearch.fields import FacetGroupsResponseField
from snosearch.fields import FiltersResponseField
from snosearch.fields import IDResponseField
from snosearch.fields import NotificationResponseField
from snovault.elasticsearch.interfaces import ELASTIC_SEARCH
from snovault.elasticsearch.searches.fields import NonSortableResponseField
from snosearch.fields import RawTopHitsResponseField
from snosearch.fields import SearchBaseResponseField
from snosearch.fields import SortResponseField
from snosearch.fields import TitleResponseField
from snosearch.fields import TypeOnlyClearFiltersResponseField
from snosearch.fields import TypeResponseField
from snosearch.parsers import ParamsParser
from snosearch.parsers import QueryString
from snosearch.responses import FieldedResponse
from snosearch.responses import FieldedGeneratorResponse

from snovault.elasticsearch.searches.interfaces import SEARCH_CONFIG

from pyramid.httpexceptions import HTTPBadRequest

from opensearch_dsl import Search


def includeme(config):
    config.add_route('search', '/search{slash:/?}')
    config.add_route('report', '/report{slash:/?}')
    config.add_route('multireport', '/multireport{slash:/?}')
    config.add_route('matrix', '/matrix{slash:/?}')
    config.add_route('missing-matrix', '/missing-matrix{slash:/?}')
    config.add_route('summary', '/summary{slash:/?}')
    config.add_route('dataset-summary', '/dataset-summary{slash:/?}')
    config.add_route('dataset-summary-agg', '/dataset-summary-agg{slash:/?}')
    config.add_route('datasets-released', '/datasets-released{slash:/?}')
    config.add_route('audit', '/audit{slash:/?}')
    config.add_route('top-hits-raw', '/top-hits-raw{slash:/?}')
    config.add_route('top-hits', '/top-hits{slash:/?}')
    config.add_route('search-config-registry', '/search-config-registry{slash:/?}')
    config.add_route('search-quick', '/search-quick{slash:/?}')
    config.scan(__name__, categories=None)


@view_config(route_name='search', request_method='GET', permission='search')
def search(context, request):
    # Note the order of rendering matters for some fields, e.g. AllResponseField and
    # NotificationResponseField depend on results from BasicSearchWithFacetsResponseField.
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title=SEARCH_TITLE
            ),
            TypeResponseField(
                at_type=[SEARCH_TITLE]
            ),
            IDResponseField(),
            ContextResponseField(),
            BasicSearchWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            ),
            AllResponseField(),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            ClearFiltersResponseField(),
            ColumnsResponseField(),
            SortResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='report', request_method='GET', permission='search')
def report(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title=REPORT_TITLE
            ),
            TypeResponseField(
                at_type=[REPORT_TITLE]
            ),
            IDResponseField(),
            ContextResponseField(),
            BasicReportWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            ),
            AllResponseField(),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            ColumnsResponseField(),
            NonSortableResponseField(),
            SortResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='multireport', request_method='GET', permission='search')
def multireport(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title=REPORT_TITLE
            ),
            TypeResponseField(
                at_type=[REPORT_TITLE]
            ),
            IDResponseField(),
            ContextResponseField(),
            MultipleTypesReportWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            ),
            AllResponseField(),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            ColumnsResponseField(),
            ResultColumnsResponseField(),
            NonSortableResponseField(),
            SortResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='matrix', request_method='GET', permission='search')
def matrix(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title=MATRIX_TITLE
            ),
            TypeResponseField(
                at_type=[MATRIX_TITLE]
            ),
            IDResponseField(),
            SearchBaseResponseField(),
            ContextResponseField(),
            BasicMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            ),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='summary', request_method='GET', permission='search')
def summary(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title=SUMMARY_TITLE
            ),
            TypeResponseField(
                at_type=[SUMMARY_TITLE]
            ),
            IDResponseField(),
            SearchBaseResponseField(),
            ContextResponseField(),
            BasicMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                matrix_definition_name=SUMMARY_MATRIX,
                reserved_keys=RESERVED_KEYS,
            ),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='audit', request_method='GET', permission='search')
def audit(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title=AUDIT_TITLE
            ),
            TypeResponseField(
                at_type=[AUDIT_TITLE]
            ),
            IDResponseField(),
            SearchBaseResponseField(),
            ContextResponseField(),
            AuditMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            ),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='top-hits-raw', request_method='GET', permission='search')
def top_hits_raw(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            RawTopHitsResponseField(
                default_item_types=TOP_HITS_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            )
        ]
    )
    return fr.render()


@view_config(route_name='top-hits', request_method='GET', permission='search')
def top_hits(context, request):
    fr = FieldedResponse(
        response_fields=[
            TypeResponseField(
                at_type=['TopHitsSearch']
            )
        ]
    )
    return fr.render()


@view_config(route_name='search-config-registry', request_method='GET', permission='search')
def search_config_registry(context, request):
    registry = request.registry[SEARCH_CONFIG]
    return dict(sorted(registry.as_dict().items()))


@view_config(route_name='search-quick', request_method='GET', permission='search')
def search_quick(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            BasicSearchResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            )
        ]
    )
    return fr.render()


def search_generator(request):
    '''
    For internal use (no view). Like search_quick but returns raw generator
    of search hits in @graph field.
    '''
    fgr = FieldedGeneratorResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            BasicSearchResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            )
        ]
    )
    return fgr.render()


@view_config(route_name='missing-matrix', request_method='GET', permission='search')
def missing_matrix(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title='Missing matrix'
            ),
            TypeResponseField(
                at_type=['MissingMatrix']
            ),
            IDResponseField(),
            SearchBaseResponseField(),
            ContextResponseField(),
            MissingMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            ),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='dataset-summary', request_method='GET', permission='search')
def dataset_summary(context, request):
    qs = QueryString(request)
    qs.clear()
    qs.extend(
        [
            ('type', 'MeasurementSet'),
            ('status!', 'deleted'),
            ('status!', 'replaced'),
            ('field', 'status'),
            ('field', 'submitted_files_timestamp'),
            ('field', 'creation_timestamp'),
            ('field', 'release_timestamp'),
            ('field', 'assay_term.term_name'),
            ('field', 'preferred_assay_title'),
            ('field', 'lab.title'),
            ('limit', 'all'),
        ]
    )
    return request.embed(f'/search-quick/?{qs.get_query_string()}', as_user='EMBED')


@view_config(route_name='dataset-summary-agg', request_method='GET', permission='search')
def dataset_summary_agg(context, request):
    qs = QueryString(request)
    qs.extend(
        [
            ('config', 'StatusFacet'),
        ]
    )
    return {
        'matrix': request.embed(f'/missing-matrix/?{qs.get_query_string()}', as_user='EMBED')['matrix']
    }


@view_config(route_name='datasets-released', request_method='GET', permission='search')
def datasets_released(context, request):
    client = request.registry[ELASTIC_SEARCH]
    search = Search(
        using=client,
        index='measurement_set'
    ).filter(
        'term',
        **{
            'embedded.status': 'released'
        }
    )[:0]
    search.aggs.bucket(
        'datasets_released',
        'date_histogram',
        field='embedded.release_timestamp',
        calendar_interval='month',
        format='MMM yyyy'
    ).pipeline(
        'cumulative_sum',
        'cumulative_sum',
        buckets_path='_count'
    )
    results = search.execute()
    return {
        'datasets_released': [
            {x['key_as_string']: x['cumulative_sum']['value']}
            for x in results.to_dict()['aggregations']['datasets_released']['buckets']
        ]
    }
