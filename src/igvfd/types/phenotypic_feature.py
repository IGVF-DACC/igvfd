from snovault import (
    collection,
    load_schema,
    calculated_property
)
from snovault.util import Path
from .base import (
    Item
)


@collection(
    name='phenotypic-features',
    properties={
        'title': 'Phenotypic Features',
        'description': 'Listing of phenotypic features',
    }
)
class PhenotypicFeature(Item):
    item_type = 'phenotypic_feature'
    schema = load_schema('igvfd:schemas/phenotypic_feature.json')
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('feature', include=['@id', 'term_id', 'term_name']),
        Path('submitted_by', include=['@id', 'title']),
    ]

    set_status_up = [
        'feature'
    ]
    set_status_down = []
