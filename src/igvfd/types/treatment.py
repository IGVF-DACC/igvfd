from snovault import (
    collection,
    load_schema,
    calculated_property
)
from .base import (
    Item
)


@collection(
    name='treatments',
    properties={
        'title': 'Treatment',
        'description': 'Listing of treatments',
    })
class Treatment(Item):
    item_type = 'treatment'
    schema = load_schema('igvfd:schemas/treatment.json')

    @calculated_property(
        schema={
            'title': 'Title',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def title(self, treatment_term_name, amount, amount_units, duration=None, duration_units=None):
        if duration is not None:
            text = 'Treated with {} {} {} for {} {}'.format(
                amount, amount_units, treatment_term_name, duration, duration_units)
        else:
            text = 'Treated with {} {} {}'.format(
                amount, amount_units, treatment_term_name)
        return text
