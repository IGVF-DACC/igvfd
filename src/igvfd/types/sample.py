from snovault import (
    collection,
    load_schema,
)

from .base import (
    Item,
)


@collection(
    name='samples',
    unique_key='sample:uuid',
    properties={
        'title': 'Samples',
        'description': 'Listing samples',
    })
class Sample(Item):
    item_type = 'sample'
    schema = load_schema('igvfd:schemas/sample.json')
