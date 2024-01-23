from snovault import (
    calculated_property,
    collection,
    load_schema,
)
from snovault.util import Path
from .base import (
    Item,
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

    set_status_up = []
    set_status_down = []

    @calculated_property(
        schema={
            'title': 'Name and Quantification',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def name_quantification(self, name, quantification):
        return u'{}-{}'.format(name, quantification)

    def unique_keys(self, properties):
        keys = super(Biomarker, self).unique_keys(properties)
        value = self.name_quantification(name=properties['name'], quantification=properties['quantification'])
        keys.setdefault('biomarker:name_quantification', []).append(value)
        return keys
