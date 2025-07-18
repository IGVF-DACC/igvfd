from snovault import (
    calculated_property,
    collection,
    load_schema,
)
from snovault.util import Path
from .base import (
    Item,
)

from igvfd.types.base import (
    Item,
    paths_filtered_by_status
)


@collection(
    name='biomarkers',
    unique_key='biomarker:name_quantification',
    properties={
        'title': 'Biomarkers',
        'description': 'Listing of biomarkers',
    })
class Biomarker(Item):
    item_type = 'biomarker'
    schema = load_schema('igvfd:schemas/biomarker.json')
    embedded_with_frame = [
        Path('award', include=['@id', 'name', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
    ]
    rev = {
        'biomarker_for': ('Biosample', 'biomarkers')
    }

    set_status_up = []
    set_status_down = []

    @calculated_property(
        schema={
            'title': 'Name and Quantification',
            'type': 'string',
            'description': 'A concatenation of the name and quantification of the biomarker.',
            'notSubmittable': True,
            'uniqueKey': True
        }
    )
    def name_quantification(self, name, quantification):
        return u'{}-{}'.format(name, quantification)

    def unique_keys(self, properties):
        keys = super(Biomarker, self).unique_keys(properties)
        value = self.name_quantification(name=properties['name'], quantification=properties['quantification'])
        keys.setdefault('biomarker:name_quantification', []).append(value)
        return keys

    @calculated_property(schema={
        'title': 'Biomarker For',
        'description': 'The samples which have been confirmed to have this biomarker.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Biomarker For',
            'type': 'string',
            'linkFrom': 'Biosample.biomarkers',
        },
        'notSubmittable': True
    })
    def biomarker_for(self, request, biomarker_for):
        return paths_filtered_by_status(request, biomarker_for)

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, name, quantification, classification=None):
        classification_phrase = ''
        if classification:
            classification_phrase = f'{classification} '
        return f'{classification_phrase}{name} {quantification}'
