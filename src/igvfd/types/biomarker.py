from snovault import (
    calculated_property,
    collection,
    load_schema,
)

from .base import (
    Item,
)


@collection(
    name='biomarkers',
    unique_key='uuid',
    properties={
        'title': 'Biomarkers',
        'description': 'Listing of biomarkers',
    })
class Biomarker(Item):
    item_type = 'biomarker'
    schema = load_schema('igvfd:schemas/biomarker.json')

    @calculated_property(
        schema={
            'title': 'Name and Quantification',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def name_quantification(self, name, quantification):
        return u'{}{}'.format(name, quantification)
