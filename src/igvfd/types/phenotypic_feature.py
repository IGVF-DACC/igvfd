from snovault import (
    collection,
    load_schema,
    calculated_property
)
from .base import (
    Item
)


@collection(
    name='phenotypic-features',
    properties={
        'title': 'Phenotypic Feature',
        'description': 'Listing of phenotypic features',
    }
)
class PhenotypicFeature(Item):
    item_type = 'phenotypic_feature'
    schema = load_schema('igvfd:schemas/phenotypic_feature.json')
