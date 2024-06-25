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
        'title': 'Treatments',
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
    rev = {
        'samples_treated': ('Sample', 'treatments')
    }

    set_status_up = []
    set_status_down = []

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, treatment_term_name, amount=None, amount_units=None, duration=None, duration_units=None):
        if duration is not None and duration != 1:
            duration_units = f'{duration_units}s'
        if amount is not None and duration is not None:
            text = f'Treatment of {amount} {amount_units} {treatment_term_name} for {duration} {duration_units}'
        elif amount is not None:
            text = f'Treatment of {amount} {amount_units} {treatment_term_name}'
        elif duration is not None:
            text = f'Depletion of {treatment_term_name} for {duration} {duration_units}'
        else:
            text = f'Depletion of {treatment_term_name}'
        return text

    @calculated_property(schema={
        'title': 'Samples Treated',
        'description': 'The samples which have been treated using this treatment.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Input to',
            'type': ['string', 'object'],
            'linkFrom': 'Samples.treatments',
        },
        'notSubmittable': True
    })
    def input_to(self, request, input_to):
        return paths_filtered_by_status(request, input_to)
