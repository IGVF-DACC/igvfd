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
<<<<<<< HEAD

    def title(self, treatment_term_name, amount, amount_units, duration=None, duration_units=None):
        if duration is not None:
            text = 'Treated with {} {} {} for {} {}'.format(
=======
    def title(self, treatment_term_name, amount, amount_units, duration, duration_units):
        if duration:
            text = 'Treated with {} {} {} for {} {}.'.format(
>>>>>>> 950b9e5 (update required)
                amount, amount_units, treatment_term_name, duration, duration_units)
        else:
            text = 'Treated with {} {} {} for non-specified duration'.format(
                amount, amount_units, treatment_term_name)
<<<<<<< HEAD
        return text

=======
        return(text)
>>>>>>> 950b9e5 (update required)
