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
        text = 'Treated with {} {} {} for {} {}.'.format(
            amount, amount_units, treatment_term_name, duration, duration_units)
        if post_treatment_time:
            text = 'Post treatment waited for {} {}.'.format(post_treatment_time, post_treatment_time_units)
        else:
            text = text
        return(text)
