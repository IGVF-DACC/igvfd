from snovault import (
    collection,
    load_schema
)
from .base import (
    Item
)


@collection(
    name='variants',
    unique_key='uuid',
    properties={
        'title': 'Variant',
        'description': 'Listing of variants',
    })
class Variant(Item):
    item_type = 'variant'
    schema = load_schema('igvfd:schemas/variant.json')
