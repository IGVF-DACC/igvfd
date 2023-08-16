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
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
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
    def title(self, purpose, treatment_term_name, amount=None, amount_units=None, duration=None, duration_units=None):
        if amount != 1:
            amount_units = amount_units = + 's'
        if duration != 1:
            duration_units = duration_units = + 's'
        if amount is not None and duration is not None:
            text = f'{purpose} treatment of {amount} {amount_units} {treatment_term_name} for {duration} {duration_units}'
        elif amount is not None:
            text = f'{purpose} treatment of {amount} {amount_units} {treatment_term_name}'
        elif duration is not None:
            text = f'{purpose} depletion of {treatment_term_name} for {duration} {duration_units}'
        else:
            text = f'{purpose} depletion of {treatment_term_name}'
        return text
