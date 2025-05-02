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

        order = ['IRB', 'PUB', 'NPU', 'MDS', 'GSO']
        sorted_modifiers = sorted(modifiers, key=order.index) if modifiers else []

        return f'{limitation}-{"-".join(sorted_modifiers)}' if sorted_modifiers else limitation

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of the institutional certificate.',
            'notSubmittable': True,
        }
    )
    def summary(self, certificate_identifier, controlled_access):
        if controlled_access:
            return certificate_identifier + ' (controlled)'
        else:
            return certificate_identifier + ' (unrestricted)'
