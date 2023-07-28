from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest

from igvfd.searches.defaults import DEFAULT_ITEM_TYPES
from igvfd.searches.defaults import RESERVED_KEYS
from igvfd.searches.defaults import TOP_HITS_ITEM_TYPES
from snosearch.interfaces import AUDIT_TITLE
from snosearch.interfaces import ITEM
from snosearch.interfaces import MATRIX_TITLE
from snosearch.interfaces import REPORT_TITLE
from snosearch.interfaces import SEARCH_TITLE
from snosearch.interfaces import SUMMARY_MATRIX
from snosearch.interfaces import SUMMARY_TITLE
from snosearch.fields import AuditMatrixWithFacetsResponseField
from snosearch.fields import AllResponseField
from snosearch.fields import BasicMatrixWithFacetsResponseField
from snosearch.fields import BasicSearchResponseField
from snosearch.fields import BasicSearchWithFacetsResponseField
from snosearch.fields import BasicReportWithFacetsResponseField
from snosearch.fields import ClearFiltersResponseField
from snosearch.fields import ColumnsResponseField
from snosearch.fields import ContextResponseField
from snosearch.fields import DebugQueryResponseField
from snosearch.fields import FacetGroupsResponseField
from snosearch.fields import FiltersResponseField
from snosearch.fields import IDResponseField
from snosearch.fields import NotificationResponseField
from snosearch.fields import RawTopHitsResponseField
from snosearch.fields import SearchBaseResponseField
from snosearch.fields import SortResponseField
from snosearch.fields import TitleResponseField
from snosearch.fields import TypeOnlyClearFiltersResponseField
from snosearch.fields import TypeResponseField
from snosearch.parsers import ParamsParser
from snosearch.responses import FieldedGeneratorResponse
from snosearch.responses import FieldedResponse

from snovault.elasticsearch.searches.fields import NonSortableResponseField
from snovault.elasticsearch.searches.interfaces import SEARCH_CONFIG
from snovault.interfaces import TYPES


def includeme(config):
    config.add_route('search', '/search{slash:/?}')
    config.add_route('report', '/report{slash:/?}')
    config.add_route('matrix', '/matrix{slash:/?}')
    config.add_route('summary', '/summary{slash:/?}')
    config.add_route('audit', '/audit{slash:/?}')
    config.add_route('top-hits-raw', '/top-hits-raw{slash:/?}')
    config.add_route('top-hits', '/top-hits{slash:/?}')
    config.add_route('search-config-registry', '/search-config-registry{slash:/?}')
    config.scan(__name__)


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
            ),
        ]
    )
    return fgr.render()


@view_config(route_name='report', request_method='GET', permission='search')
def report(context, request):
    validate_report(request)
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


def validate_report(request):
    item_registry = request.registry[TYPES]
    types_to_query = request.params.getall('type')
    if ITEM in types_to_query:
        msg = 'Report view does not support Item type'
        raise HTTPBadRequest(explanation=msg)
    if len(types_to_query) > 1:
        abstract_types = item_registry.abstract
        subtypes_to_query = []
        for item_type in types_to_query:
            if item_type in abstract_types:
                for obj in abstract_types[item_type].subtypes:
                    if obj not in subtypes_to_query:
                        subtypes_to_query.append(obj)
            elif item_type not in subtypes_to_query:
                subtypes_to_query.append(item_type)
        is_logic_group = False
        for item_type in abstract_types:
            subtypes = abstract_types[item_type].subtypes
            if len(subtypes) == 1 or item_type == 'Item':
                continue
            is_logic_group = True
            for subtype in subtypes_to_query:
                if subtype not in subtypes:
                    is_logic_group = False
                    break
            if is_logic_group:
                break
        if not is_logic_group:
            msg = f'Report view does not support the group of types: {types_to_query}'
            raise HTTPBadRequest(explanation=msg)
