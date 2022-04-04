from snovault import (
    collection,
    load_schema,
    calculated_property
)
from .base import (
    Item,
    paths_filtered_by_status,
    ALLOW_CURRENT,
    DELETED,
)


@collection(
    name='sources',
    unique_key='source:name',
    properties={
        'title': 'Sources',
        'description': 'Listing of sources',
    }
)
class Source(Item):
    item_type = 'source'
    schema = load_schema('igvfd:schemas/source.json')
