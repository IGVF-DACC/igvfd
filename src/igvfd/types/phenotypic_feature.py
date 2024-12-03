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
        Path('feature', include=['@id', 'term_id', 'term_name', 'status']),
        Path('submitted_by', include=['@id', 'title']),
    ]

    set_status_up = [
        'feature'
    ]
    set_status_down = []

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, feature, quantity=None, quantity_units=None, observation_date=None):
        feature_object = request.embed(feature)
        quantity_phrase = ''
        if quantity:
            quantity_phrase = f'{quantity} {quantity_units} '
        date_phrase = ''
        if observation_date:
            date_phrase = f' observed on {observation_date}'
        return f'{quantity_phrase}{feature_object["term_name"]}{date_phrase}'
