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
    name='treatments',
    properties={
        'title': 'Treatment',
        'description': 'Listing of treatments',
    }
)
class Treatment(Item):
    item_type = 'treatment'
    schema = load_schema('igvfd:schemas/treatment.json')
    embedded_with_frame = [
        Path('sources', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
    ]

    @calculated_property(
        schema={
            'title': 'Title',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def title(self, treatment_term_name, amount=None, amount_units=None, duration=None, duration_units=None):
        if duration is not None and amount is not None:
            text = 'Treated with {} {} {} for {} {}'.format(
                amount, amount_units, treatment_term_name, duration, duration_units)
        elif duration is None and amount is not None:
            text = 'Treated with {} {} {}'.format(
                amount, amount_units, treatment_term_name)
        elif amount is None and duration is not None:
            text = 'Depleted in {} for {} {}'.format(
                treatment_term_name, duration, duration_units)
        elif amount is None and duration is None:
            text = 'Depleted in {}'.format(
                treatment_term_name)
        return text
