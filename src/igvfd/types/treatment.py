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
    unique_key='uuid',
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
        }
    )
    def title(self, treatment_term_name, amount, amount_units, duration, duration_units):
        text = f'{treatment_term_name} {amount} {amount_units} {duration} {duration_units} '
