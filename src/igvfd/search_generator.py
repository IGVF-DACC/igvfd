from snosearch.responses import FieldedGeneratorResponse
from snosearch.parsers import ParamsParser
from snosearch.fields import BasicSearchResponseField
from igvfd.searches.defaults import DEFAULT_ITEM_TYPES
from igvfd.searches.defaults import RESERVED_KEYS


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
