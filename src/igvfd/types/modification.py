from snovault import (
    collection,
    load_schema,
    calculated_property
)
from .base import (
    Item
)


@collection(
    name='modifications',
    properties={
        'title': 'Modification',
        'description': 'Listing of modifications',
    }
)
class Modification(Item):
    item_type = 'modification'
    schema = load_schema('igvfd:schemas/modification.json')
