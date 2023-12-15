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
    unique_key='institutional_certification:number',
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

    def unique_keys(self, properties):
        keys = super(InstitutionalCertificate, self).unique_keys(properties)
        keys.setdefault('institutional_certification:number', []).append(properties['number'])
        return keys
