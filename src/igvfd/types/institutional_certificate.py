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
    name='institutional-certificates',
    unique_key='institutional_certification:certificate_identifier',
    properties={
        'title': 'Institutional Certificates',
        'description': 'Listing of institutional certificates',
    }
)
class InstitutionalCertificate(Item):
    item_type = 'institutional_certificate'
    schema = load_schema('igvfd:schemas/institutional_certificate.json')
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
    ]

    set_status_up = []
    set_status_down = []

    @calculated_property(schema={
        'title': 'Data Use Limitation Summary',
        'type': 'string',
        'description': 'A combination of the data use limitation and its modifiers',
        'notSubmittable': True,
    })
    def data_use_limitation_summary(self, properties=None):
        if properties is None:
            properties = self.upgrade_properties()
        limitation = properties.get('data_use_limitation', 'No limitations')
        modifiers = properties.get('data_use_limitation_modifiers', [])
        joined_modifiers = ','.join(modifiers) if modifiers else ''
        return f'{limitation}-{joined_modifiers}' if joined_modifiers else limitation

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of the institutional certificate.',
            'notSubmittable': True,
        }
    )
    def summary(self, title, certificate_identifier, controlled_access):
        if self.controlled_access:
            return self.certificate_identifier + ' (controlled)'
        else:
            return self.certificate_identifier + ' (unrestricted)'
