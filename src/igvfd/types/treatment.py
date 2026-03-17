from snovault import (
    collection,
    load_schema,
    calculated_property
)
from snovault.util import Path
from .base import (
    Item
)

from igvfd.types.base import (
    Item,
    paths_filtered_by_status
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
        Path('sources', include=['@id', 'title', 'status']),
        Path('submitted_by', include=['@id', 'title']),
    ]
    rev = {
        'biosamples_treated': ('Biosample', 'treatments')
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
    def summary(
        self,
        treatment_term_name,
        treatment_type=None,
        depletion=False,
        amount=None,
        amount_units=None,
        duration=None,
        duration_units=None,
        temperature=None,
        temperature_units=None,
    ):
        # Pluralize duration_units when duration != 1 (e.g. "minute" -> "minutes")
        if duration is not None and duration_units is not None and duration != 1:
            duration_units_display = f'{duration_units}s'
        else:
            duration_units_display = duration_units

        # Depletion treatments: always "Depletion of ..."
        if depletion:
            if duration is not None and duration_units_display is not None:
                return f'Depletion of {treatment_term_name} for {duration} {duration_units_display}'
            return f'Depletion of {treatment_term_name}'

        # Non-depletion: always "Treatment of ..."
        # Amount + duration + temperature
        if amount is not None and amount_units is not None and duration is not None and temperature is not None:
            return (
                f'Treatment of {amount} {amount_units} {treatment_term_name} '
                f'for {duration} {duration_units_display} at {temperature} {temperature_units}'
            )
        # Amount + duration
        if amount is not None and amount_units is not None and duration is not None:
            return (
                f'Treatment of {amount} {amount_units} {treatment_term_name} '
                f'for {duration} {duration_units_display}'
            )
        # Amount + temperature (no duration)
        if amount is not None and amount_units is not None and temperature is not None:
            return (
                f'Treatment of {amount} {amount_units} {treatment_term_name} '
                f'at {temperature} {temperature_units}'
            )
        # Temperature + duration (heat exposure style)
        if amount is None and temperature is not None and duration is not None:
            return (
                f'Treatment of heat exposure at {temperature} {temperature_units} '
                f'for {duration} {duration_units_display}'
            )
        # Amount only
        if amount is not None and amount_units is not None:
            return f'Treatment of {amount} {amount_units} {treatment_term_name}'
        # Temperature only (heat exposure)
        if temperature is not None:
            return f'Treatment of heat exposure at {temperature} {temperature_units}'
        # Diet or other duration-only treatment
        if treatment_type == 'diet' or duration is not None:
            if duration is not None and duration_units_display is not None:
                return f'Treatment of {treatment_term_name} for {duration} {duration_units_display}'
            return f'Treatment of {treatment_term_name}'
        # Fallback: treatment with only term name
        return f'Treatment of {treatment_term_name}'

    @calculated_property(schema={
        'title': 'Biosamples Treated',
        'description': 'The samples which have been treated using this treatment.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Biosamples Treated',
            'type': 'string',
            'linkFrom': 'Biosample.treatments',
        },
        'notSubmittable': True
    })
    def biosamples_treated(self, request, biosamples_treated):
        return paths_filtered_by_status(request, biosamples_treated)
