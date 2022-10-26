from snovault.attachment import ItemWithAttachment
from snovault import (
    collection,
    load_schema,
)
from .base import (
    Item,
    paths_filtered_by_status,
    ALLOW_CURRENT,
    DELETED,
)


@collection(
    name='curated-sets',
    properties={
        'title': 'Curated Set',
        'description': 'Listing of curated sets',
    })
class CuratedSet(ItemWithAttachment, Item):
    item_type = 'curated_set'
    schema = load_schema('igvfd:schemas/curated_set.json')
